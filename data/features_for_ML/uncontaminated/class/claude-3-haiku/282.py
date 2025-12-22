import json

class CreateOrder:
    def __init__(self, order_id: str, customer_name: str, items: list, total_amount: float):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.total_amount = total_amount

    @classmethod
    def from_json(cls, json_str: str) -> 'CreateOrder':
        data = json.loads(json_str)
        return cls(
            order_id=data['order_id'],
            customer_name=data['customer_name'],
            items=data['items'],
            total_amount=data['total_amount']
        )

    def to_json(self) -> str:
        data = {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'items': self.items,
            'total_amount': self.total_amount
        }
        return json.dumps(data)