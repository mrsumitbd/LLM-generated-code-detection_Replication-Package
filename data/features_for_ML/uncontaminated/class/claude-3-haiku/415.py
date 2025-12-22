from collections import defaultdict
from typing import Iterable

class Order:
    def __init__(self, id: str, price: float, stop: float):
        self.id = id
        self.price = price
        self.stop = stop

class PriceOrderBook:
    """
    Price-based sorted order storage.
    An order can appear multiple times at different prices.
    """

    def __init__(self):
        self.orders = defaultdict(list)

    def add_order(self, order: Order):
        self.orders[order.price].append(order)

    def remove_order(self, order: Order):
        orders_at_price = self.orders[order.price]
        orders_at_price.remove(order)
        if not orders_at_price:
            del self.orders[order.price]

    def update_order_stop(self, order: Order, new_stop: float):
        self.remove_order(order)
        order.stop = new_stop
        self.add_order(order)

    def iter_orders(self, *, desc=False, min_price: float | None = None, max_price: float | None = None) -> Iterable[Order]:
        prices = sorted(self.orders.keys(), reverse=desc)
        for price in prices:
            if (min_price is None or price >= min_price) and (max_price is None or price <= max_price):
                for order in self.orders[price]:
                    yield order

    def clear(self):
        self.orders.clear()