import json

class CreateOrder:
    def __init__(self):
        self.data = {}

    @classmethod
    def from_json(cls, json_str: str) -> 'CreateOrder':
        instance = cls()
        instance.data = json.loads(json_str)
        return instance

    def to_json(self) -> str:
        return json.dumps(self.data)