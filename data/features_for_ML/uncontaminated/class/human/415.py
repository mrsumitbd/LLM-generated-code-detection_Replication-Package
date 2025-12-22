from collections import deque, defaultdict
from bisect import insort, bisect_left

class PriceOrderBook:
    """
    Price-based sorted order storage.
    An order can appear multiple times at different prices.
    """

    __slots__ = ('price_levels', 'orders_at_price', 'order_prices')

    def __init__(self):
        self.price_levels = []  # Sorted list of prices
        self.orders_at_price = defaultdict(list)  # price -> [Order]
        self.order_prices = defaultdict(set)  # Order -> {prices}

    def add_order(self, order: Order):
        """Add order to all its relevant price levels"""
        # Add to stop price if exists
        if order.stop is not None:
            price = order.stop
            if price not in self.orders_at_price:
                insort(self.price_levels, price)
            self.orders_at_price[price].append(order)
            self.order_prices[order].add(price)

        # Add to limit price if exists
        if order.limit is not None:
            price = order.limit
            if price not in self.orders_at_price:
                insort(self.price_levels, price)
            self.orders_at_price[price].append(order)
            self.order_prices[order].add(price)

        # Add to trail price if exists
        if order.trail_price is not None:
            price = order.trail_price
            if price not in self.orders_at_price:
                insort(self.price_levels, price)
            self.orders_at_price[price].append(order)
            self.order_prices[order].add(price)

    def remove_order(self, order: Order):
        """Remove order from all price levels"""
        for price in list(self.order_prices[order]):
            self.orders_at_price[price].remove(order)
            if not self.orders_at_price[price]:
                idx = bisect_left(self.price_levels, price)
                if idx < len(self.price_levels) and self.price_levels[idx] == price:
                    del self.price_levels[idx]
                del self.orders_at_price[price]
        del self.order_prices[order]

    def update_order_stop(self, order: Order, new_stop: float):
        """Update the stop price of an order in the order book"""
        # Remove the order from the old stop price level if it exists
        if order.stop is not None and order.stop in self.order_prices[order]:
            old_stop = order.stop
            self.orders_at_price[old_stop].remove(order)
            self.order_prices[order].remove(old_stop)
            if not self.orders_at_price[old_stop]:
                idx = bisect_left(self.price_levels, old_stop)
                if idx < len(self.price_levels) and self.price_levels[idx] == old_stop:
                    del self.price_levels[idx]
                del self.orders_at_price[old_stop]

        # Update the order's stop price
        order.stop = new_stop

        # Add the order to the new stop price level
        if new_stop not in self.orders_at_price:
            insort(self.price_levels, new_stop)
        self.orders_at_price[new_stop].append(order)
        self.order_prices[order].add(new_stop)

    def iter_orders(self, *, desc=False, min_price: float | None = None, max_price: float | None = None):
        """
        Iterate over orders within price range.

        Examples:
            iter_orders()  # All orders, ascending
            iter_orders(desc=True)  # All orders, descending
            iter_orders(min_price=50.0)  # 50, 51, 52, ... (ascending)
            iter_orders(max_price=60.0)  # 60, 59, 58, ... (descending)
            iter_orders(min_price=50.0, max_price=60.0)  # 50, 51, ..., 60 (ascending)

        :param desc: If True, iterate in descending order, only if no min_price or max_price is set
        :param min_price: If set, iterate from this price upward (ascending)
        :param max_price: If set, iterate from this price downward (descending)
        :return: Generator yielding Order objects
        """
        if min_price is not None and max_price is not None:
            # Range query - ascending from min to max
            min_idx = bisect_left(self.price_levels, min_price)
            max_idx = bisect_left(self.price_levels, max_price)
            # Include max_price if it matches exactly
            if max_idx < len(self.price_levels) and self.price_levels[max_idx] == max_price:
                max_idx += 1
            # Create a copy of price levels to avoid iteration issues when levels are removed
            for p in list(self.price_levels[min_idx:max_idx]):
                # Create a copy to avoid iteration issues when orders are removed during iteration
                yield from list(self.orders_at_price[p])

        elif min_price is not None:
            # Ascending from min_price
            min_idx = bisect_left(self.price_levels, min_price)
            # Create a copy of price levels to avoid iteration issues when levels are removed
            for p in list(self.price_levels[min_idx:]):
                # Create a copy to avoid iteration issues when orders are removed during iteration
                yield from list(self.orders_at_price[p])

        elif max_price is not None:
            # Descending from max_price
            max_idx = bisect_left(self.price_levels, max_price)
            # Include max_price if it matches exactly
            if max_idx < len(self.price_levels) and self.price_levels[max_idx] == max_price:
                max_idx += 1
            # Iterate in reverse order (high to low prices)
            # Create a copy of price levels to avoid iteration issues when levels are removed
            # Note: reversed() already creates an iterator over a copy of the slice
            for p in reversed(list(self.price_levels[:max_idx])):
                # Create a copy to avoid iteration issues when orders are removed during iteration
                yield from list(self.orders_at_price[p])

        elif desc:
            # All orders, descending
            # Create a copy of price levels to avoid iteration issues when levels are removed
            for p in reversed(list(self.price_levels)):
                # Create a copy to avoid iteration issues when orders are removed during iteration
                yield from list(self.orders_at_price[p])
        else:
            # All orders, ascending
            # Create a copy of price levels to avoid iteration issues when levels are removed
            for p in list(self.price_levels):
                # Create a copy to avoid iteration issues when orders are removed during iteration
                yield from list(self.orders_at_price[p])

    def clear(self):
        """Clear all orders"""
        self.price_levels.clear()
        self.orders_at_price.clear()
        self.order_prices.clear()