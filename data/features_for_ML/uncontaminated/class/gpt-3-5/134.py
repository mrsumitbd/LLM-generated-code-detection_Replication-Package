class BaseConfig:
    
    @staticmethod
    def from_dict(config_class, config_dict):
        instance = config_class()
        for key, value in config_dict.items():
            setattr(instance, key, value)
        return instance