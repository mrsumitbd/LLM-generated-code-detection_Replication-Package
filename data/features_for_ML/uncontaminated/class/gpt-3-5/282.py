class CreateOrder:

    def __init__(self):
        pass

    @classmethod
    def from_json(cls, json_str: str) -> 'CreateOrder':
        order = cls()
        # Parse json_str and set attributes of order object
        return order

    def to_json(self) -> str:
        # Convert attributes of self to a JSON string
        return json_str