import json
from typing import Any, Dict


class Config:
    """
    A simple configuration container that can be serialized to and from JSON.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the configuration with arbitrary keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self) -> str:
        """
        Serialize the configuration to a JSON string.
        """
        # Convert the instance's __dict__ to JSON.
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str) -> "Config":
        """
        Deserialize a JSON string into a Config instance.
        """
        if not isinstance(data, str):
            raise TypeError("data must be a JSON string")

        try:
            obj = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

        if not isinstance(obj, dict):
            raise ValueError("JSON data must represent an object")

        # Create a new Config instance and set attributes.
        cfg = Config()
        for key, value in obj.items():
            setattr(cfg, key, value)

        return cfg

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"