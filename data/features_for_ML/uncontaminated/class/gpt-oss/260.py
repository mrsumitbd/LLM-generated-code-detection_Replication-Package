import inspect
from typing import Dict, List, Type
from pydantic import BaseModel


class SchemaRegistry:
    """Registry for managing schema contracts and versions."""

    _registry: Dict[str, Dict[str, Type[BaseModel]]] = {}

    @classmethod
    def register(cls, name: str, version: str) -> None:
        """
        Register a schema class defined in the caller's module.
        The class must be named ``<name>_<version>`` and inherit from BaseModel.
        """
        # Find the caller's module
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        if module is None:
            raise RuntimeError("Cannot determine caller module for schema registration")

        # Build the expected class name
        class_name = f"{name}_{version}"
        schema_cls = getattr(module, class_name, None)

        if schema_cls is None:
            raise ValueError(f"Schema class '{class_name}' not found in module '{module.__name__}'")
        if not issubclass(schema_cls, BaseModel):
            raise TypeError(f"Schema class '{class_name}' must inherit from pydantic.BaseModel")

        cls._registry.setdefault(name, {})[version] = schema_cls

    @classmethod
    def get_schema(cls, name: str, version: str) -> Type[BaseModel]:
        """Return the registered schema class for the given name and version."""
        try:
            return cls._registry[name][version]
        except KeyError:
            raise KeyError(f"Schema '{name}' with version '{version}' is not registered")

    @classmethod
    def get_available_schemas(cls) -> List[str]:
        """Return a list of all registered schema names."""
        return list(cls._registry.keys())

    @classmethod
    def get_schemas_for_destination(cls, name: str) -> List[str]:
        """Return a list of all registered versions for the given schema name."""
        try:
            return list(cls._registry[name].keys())
        except KeyError:
            raise KeyError(f"No schemas registered for destination '{name}'")

    @classmethod
    def get_available_destinations(cls) -> List[str]:
        """Return a list of all registered destinations (schema names)."""
        return cls.get_available_schemas()

    @classmethod
    def is_registered(cls, name: str, version: str) -> bool:
        """Check if a schema with the given name and version is registered."""
        return name in cls._registry and version in cls._registry[name]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered schemas."""
        cls._registry.clear()