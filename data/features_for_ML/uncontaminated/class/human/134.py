from dataclasses import dataclass, field, fields

class BaseConfig:
    @staticmethod
    def from_dict(config_class, config_dict):
        field_names = {f.name for f in fields(config_class)}
        filtered_dict = {k: v for k, v in config_dict.items() if k in field_names}
        return config_class(**filtered_dict)