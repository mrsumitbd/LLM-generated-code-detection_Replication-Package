from typing import List

class SchemaRegistry:
    _schemas = {}

    @classmethod
    def register(cls, name: str, version: str):
        cls._schemas.setdefault(name, []).append(version)

    @classmethod
    def get_schema(cls, name: str, version: str) -> type:
        return BaseModel

    @classmethod
    def get_available_schemas(cls) -> List[str]:
        return list(cls._schemas.keys())

    @classmethod
    def get_schemas_for_destination(cls, name: str) -> List[str]:
        return cls._schemas.get(name, [])

    @classmethod
    def get_available_destinations(cls) -> List[str]:
        return list(cls._schemas.keys())

    @classmethod
    def is_registered(cls, name: str, version: str) -> bool:
        return version in cls._schemas.get(name, [])

    @classmethod
    def clear(cls) -> None:
        cls._schemas = {}