from typing import Dict, Set
from pydantic import BaseModel


class SchemaRegistry:
    """Registry for managing schema contracts and versions."""

    _schemas: Dict[str, Dict[str, type[BaseModel]]] = {}
    _destinations: Dict[str, Set[str]] = {}

    @classmethod
    def register(cls, name: str, version: str):
        """Decorator to register a schema with a name and version."""
        def decorator(schema_class: type[BaseModel]) -> type[BaseModel]:
            if name not in cls._schemas:
                cls._schemas[name] = {}
            cls._schemas[name][version] = schema_class
            
            if name not in cls._destinations:
                cls._destinations[name] = set()
            cls._destinations[name].add(version)
            
            return schema_class
        return decorator

    @classmethod
    def get_schema(cls, name: str, version: str) -> type[BaseModel]:
        """Retrieve a schema by name and version."""
        if name not in cls._schemas or version not in cls._schemas[name]:
            raise ValueError(f"Schema '{name}' with version '{version}' not found")
        return cls._schemas[name][version]

    @classmethod
    def get_available_schemas(cls) -> list[str]:
        """Get list of all registered schema names."""
        return list(cls._schemas.keys())

    @classmethod
    def get_schemas_for_destination(cls, name: str) -> list[str]:
        """Get list of all versions for a specific schema name."""
        if name not in cls._schemas:
            return []
        return list(cls._schemas[name].keys())

    @classmethod
    def get_available_destinations(cls) -> list[str]:
        """Get list of all available destination names."""
        return list(cls._destinations.keys())

    @classmethod
    def is_registered(cls, name: str, version: str) -> bool:
        """Check if a schema with given name and version is registered."""
        return name in cls._schemas and version in cls._schemas[name]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered schemas."""
        cls._schemas.clear()
        cls._destinations.clear()