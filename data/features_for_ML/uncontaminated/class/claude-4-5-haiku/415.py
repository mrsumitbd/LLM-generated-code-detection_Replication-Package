class PriceOrderBook:
    """
    Price-based sorted order storage.
    An order can appear multiple times at different prices.
    """

    def __init__(self):
        self._orders = {}  # price -> list of orders

    def add_order(self, order: Order):
        price = order.stop
        if price not in self._orders:
            self._orders[price] = []
        self._orders[price].append(order)

    def remove_order(self, order: Order):
        price = order.stop
        if price in self._orders:
            if order in self._orders[price]:
                self._orders[price].remove(order)
            if not self._orders[price]:
                del self._orders[price]

    def update_order_stop(self, order: Order, new_stop: float):
        self.remove_order(order)
        order.stop = new_stop
        self.add_order(order)

    def iter_orders(self, *, desc=False, min_price: float | None = None, max_price: float | None = None):
        prices = sorted(self._orders.keys(), reverse=desc)
        
        for price in prices:
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            
            for order in self._orders[price]:
                yield order

    def clear(self):
        self._orders.clear()