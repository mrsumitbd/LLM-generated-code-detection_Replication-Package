import json

class Config:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str):
        return Config(**json.loads(data))