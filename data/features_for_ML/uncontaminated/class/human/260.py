from pydantic import BaseModel

class SchemaRegistry:
    """Registry for managing schema contracts and versions."""

    _schemas: dict[str, dict[str, type[BaseModel]]] = {}

    @classmethod
    def register(cls, name: str, version: str):
        """Decorator to register a schema class for a specific destination and version.

        Args:
            name (str): The destination/exporter name (e.g., "elasticsearch")
            version (str): The version string (e.g., "1.0", "1.1")

        Returns:
            The decorator function
        """

        def decorator(schema_cls: type[T]) -> type[T]:
            if name not in cls._schemas:
                cls._schemas[name] = {}

            if version in cls._schemas[name]:
                logger.warning("Overriding existing schema for %s:%s", name, version)

            cls._schemas[name][version] = schema_cls
            logger.debug("Registered schema %s for %s:%s", schema_cls.__name__, name, version)

            return schema_cls

        return decorator

    @classmethod
    def get_schema(cls, name: str, version: str) -> type[BaseModel]:
        """Get the schema class for a specific destination and version.

        Args:
            name (str): The destination/exporter name (e.g., "elasticsearch")
            version (str): The version string to look up

        Returns:
            type[BaseModel]: The Pydantic model class for the requested destination and version

        Raises:
            KeyError: If the name:version combination is not registered.
        """
        if name not in cls._schemas:
            available_destinations = list(cls._schemas.keys())
            raise KeyError(f"Destination '{name}' not found. "
                           f"Available destinations: {available_destinations}")

        if version not in cls._schemas[name]:
            available_versions = list(cls._schemas[name].keys())
            raise KeyError(f"Version '{version}' not found for destination '{name}'. "
                           f"Available versions: {available_versions}")

        return cls._schemas[name][version]

    @classmethod
    def get_available_schemas(cls) -> list[str]:
        """Get all registered schema name:version combinations.

        Returns:
            list[str]: List of registered schema keys in "name:version" format
        """
        schemas = []
        for name, versions in cls._schemas.items():
            for version in versions.keys():
                schemas.append(f"{name}:{version}")
        return schemas

    @classmethod
    def get_schemas_for_destination(cls, name: str) -> list[str]:
        """Get all registered schema versions for a specific destination.

        Args:
            name (str): The destination/exporter name

        Returns:
            list[str]: List of version strings for the specified destination
        """
        if name not in cls._schemas:
            return []
        return list(cls._schemas[name].keys())

    @classmethod
    def get_available_destinations(cls) -> list[str]:
        """Get all registered destination names.

        Returns:
            list[str]: List of registered destination names
        """
        return list(cls._schemas.keys())

    @classmethod
    def is_registered(cls, name: str, version: str) -> bool:
        """Check if a name:version combination is registered.

        Args:
            name (str): The destination/exporter name
            version (str): The version string to check

        Returns:
            bool: True if the name:version is registered, False otherwise
        """
        return name in cls._schemas and version in cls._schemas[name]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered schemas."""
        cls._schemas.clear()