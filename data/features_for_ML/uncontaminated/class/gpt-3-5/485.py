class ModelArgs:
    
    def __post_init__(self):
        pass

    @classmethod
    def from_name(cls, name: str):
        return cls()