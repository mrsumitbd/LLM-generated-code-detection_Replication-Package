class Config:
    
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return self.data

    @staticmethod
    def from_json(data: str):
        return Config(data)