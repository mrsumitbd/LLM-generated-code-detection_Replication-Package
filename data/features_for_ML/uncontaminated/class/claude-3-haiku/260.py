from typing import Type
from pydantic import BaseModel

class SchemaRegistry:
    """Registry for managing schema contracts and versions."""
    _schemas = {}
    _destinations = set()

    @classmethod
    def register(cls, name: str, version: str):
        key = f"{name}:{version}"
        if key in cls._schemas:
            raise ValueError(f"Schema '{name}' version '{version}' already registered.")
        cls._schemas[key] = None
        cls._destinations.add(name)

    @classmethod
    def get_schema(cls, name: str, version: str) -> Type[BaseModel]:
        key = f"{name}:{version}"
        if key not in cls._schemas:
            raise ValueError(f"Schema '{name}' version '{version}' is not registered.")
        if cls._schemas[key] is None:
            raise ValueError(f"Schema '{name}' version '{version}' has not been set.")
        return cls._schemas[key]

    @classmethod
    def get_available_schemas(cls) -> list[str]:
        return list(cls._schemas.keys())

    @classmethod
    def get_schemas_for_destination(cls, name: str) -> list[str]:
        return [k for k in cls._schemas if k.startswith(f"{name}:")]

    @classmethod
    def get_available_destinations(cls) -> list[str]:
        return list(cls._destinations)

    @classmethod
    def is_registered(cls, name: str, version: str) -> bool:
        key = f"{name}:{version}"
        return key in cls._schemas

    @classmethod
    def clear(cls) -> None:
        cls._schemas.clear()
        cls._destinations.clear()

    @classmethod
    def set_schema(cls, name: str, version: str, schema: Type[BaseModel]):
        key = f"{name}:{version}"
        if key not in cls._schemas:
            raise ValueError(f"Schema '{name}' version '{version}' is not registered.")
        cls._schemas[key] = schema