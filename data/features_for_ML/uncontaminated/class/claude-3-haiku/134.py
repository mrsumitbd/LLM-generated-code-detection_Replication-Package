class BaseConfig:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(config_class, config_dict):
        return config_class(**config_dict)