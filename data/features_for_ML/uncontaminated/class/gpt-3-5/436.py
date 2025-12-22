from pathlib import Path
from typing import List, Union

DecoratedFunction = None  # Placeholder for DecoratedFunction type


class CodemodManager:
    """Manages codemod operations in the local filesystem."""

    @staticmethod
    def get_valid_name(name: str) -> str:
        pass

    @classmethod
    def get_codemod(cls, name: str, start_path: Path | None = None) -> DecoratedFunction:
        pass

    @classmethod
    def list(cls, start_path: Path | None = None) -> List[DecoratedFunction]:
        pass

    @classmethod
    def get(cls, name: str, start_path: Path | None = None) -> Union[DecoratedFunction, None]:
        pass

    @classmethod
    def exists(cls, name: str, start_path: Path | None = None) -> bool:
        pass

    @classmethod
    def get_decorated(cls, start_path: Path | None = None) -> List[DecoratedFunction]:
        pass