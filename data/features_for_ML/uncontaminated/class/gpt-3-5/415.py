from typing import List

class Order:
    def __init__(self, order_id: int, price: float, stop: float):
        self.order_id = order_id
        self.price = price
        self.stop = stop

class PriceOrderBook:
    """
    Price-based sorted order storage.
    An order can appear multiple times at different prices.
    """

    def __init__(self):
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)
        self.orders.sort(key=lambda x: x.price)

    def remove_order(self, order: Order):
        self.orders = [o for o in self.orders if o.order_id != order.order_id]

    def update_order_stop(self, order: Order, new_stop: float):
        for o in self.orders:
            if o.order_id == order.order_id:
                o.stop = new_stop

    def iter_orders(self, *, desc=False, min_price=None, max_price=None):
        filtered_orders = self.orders
        if min_price is not None:
            filtered_orders = [o for o in filtered_orders if o.price >= min_price]
        if max_price is not None:
            filtered_orders = [o for o in filtered_orders if o.price <= max_price]
        if desc:
            filtered_orders.reverse()
        return filtered_orders

    def clear(self):
        self.orders = []