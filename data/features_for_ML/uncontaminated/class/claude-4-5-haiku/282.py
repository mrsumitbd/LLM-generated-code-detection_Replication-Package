import json
from typing import Any, Dict, Optional

class CreateOrder:
    def __init__(
        self,
        order_id: Optional[str] = None,
        customer_name: Optional[str] = None,
        items: Optional[list] = None,
        total_amount: Optional[float] = None,
        status: Optional[str] = None,
        **kwargs
    ):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items or []
        self.total_amount = total_amount
        self.status = status or "pending"
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_json(cls, json_str: str) -> 'CreateOrder':
        data = json.loads(json_str)
        return cls(**data)

    def to_json(self) -> str:
        data = {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status
        }
        return json.dumps(data)