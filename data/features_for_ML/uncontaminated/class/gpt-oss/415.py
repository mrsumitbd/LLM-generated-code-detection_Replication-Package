class PriceOrderBook:
    """
    Price-based sorted order storage.
    An order can appear multiple times at different prices.
    """

    def __init__(self):
        # Mapping from price to a set of orders at that price
        self._orders_by_price: dict[float, set] = {}

    def add_order(self, order: "Order"):
        """
        Add an order to the book. The order is stored under its current price.
        """
        price = order.price
        self._orders_by_price.setdefault(price, set()).add(order)

    def remove_order(self, order: "Order"):
        """
        Remove an order from the book. If the order is not present, the call is ignored.
        """
        price = order.price
        orders = self._orders_by_price.get(price)
        if orders and order in orders:
            orders.remove(order)
            if not orders:
                del self._orders_by_price[price]

    def update_order_stop(self, order: "Order", new_stop: float):
        """
        Update the stop price of an order. The order remains at its current price.
        """
        order.stop = new_stop

    def iter_orders(
        self,
        *,
        desc: bool = False,
        min_price: float | None = None,
        max_price: float | None = None,
    ):
        """
        Iterate over all orders in the book, sorted by price.

        Parameters
        ----------
        desc : bool, optional
            If True, iterate from highest to lowest price. Default is False.
        min_price : float, optional
            Minimum price to include. If None, no lower bound.
        max_price : float, optional
            Maximum price to include. If None, no upper bound.
        """
        prices = sorted(self._orders_by_price.keys(), reverse=desc)
        for price in prices:
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            for order in self._orders_by_price[price]:
                yield order

    def clear(self):
        """
        Remove all orders from the book.
        """
        self._orders_by_price.clear()