import builtins
import importlib.util
import os
import sys
import types
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

# Type alias for a function that has been decorated as a codemod
DecoratedFunction = Callable[..., Any]


class CodemodManager:
    """Manages codemod operations in the local filesystem."""

    @staticmethod
    def get_valid_name(name: str) -> str:
        """
        Normalise a codemod name:
        - Strip leading/trailing whitespace
        - Convert to lowercase
        - Replace spaces and hyphens with underscores
        - Remove any characters that are not alphanumeric or underscore
        """
        import re

        name = name.strip().lower()
        name = re.sub(r"[ -]+", "_", name)
        name = re.sub(r"[^a-z0-9_]", "", name)
        return name

    @classmethod
    def _iter_codemod_files(cls, start_path: Optional[Path]) -> List[Path]:
        """
        Return a list of all .py files under start_path (recursively).
        If start_path is None, use the current working directory.
        """
        base = start_path or Path.cwd()
        return [p for p in base.rglob("*.py") if p.is_file()]

    @classmethod
    def _load_module_from_path(cls, path: Path) -> types.ModuleType:
        """
        Dynamically load a module from a given file path.
        """
        spec = importlib.util.spec_from_file_location(path.stem, str(path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)  # type: ignore
        return module

    @classmethod
    def _find_codemod_functions(
        cls, start_path: Optional[Path]
    ) -> List[DecoratedFunction]:
        """
        Discover all functions in the filesystem that have been decorated
        as codemods. A codemod function is identified by having an attribute
        `__codemod_name__` set by the decorator.
        """
        codemods: List[DecoratedFunction] = []
        for file_path in cls._iter_codemod_files(start_path):
            try:
                module = cls._load_module_from_path(file_path)
            except Exception:
                continue  # Skip files that cannot be imported
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, "__codemod_name__"):
                    codemods.append(attr)
        return codemods

    @classmethod
    def list(cls, start_path: Optional[Path] = None) -> builtins.list[DecoratedFunction]:
        """
        Return a list of all discovered codemod functions.
        """
        return cls._find_codemod_functions(start_path)

    @classmethod
    def get(
        cls, name: str, start_path: Optional[Path] = None
    ) -> Optional[DecoratedFunction]:
        """
        Return the codemod function with the given name, or None if not found.
        """
        valid_name = cls.get_valid_name(name)
        for func in cls._find_codemod_functions(start_path):
            if getattr(func, "__codemod_name__", None) == valid_name:
                return func
        return None

    @classmethod
    def get_codemod(cls, name: str, start_path: Optional[Path] = None) -> DecoratedFunction:
        """
        Return the codemod function with the given name.
        Raises a KeyError if not found.
        """
        func = cls.get(name, start_path)
        if func is None:
            raise KeyError(f"Codemod '{name}' not found")
        return func

    @classmethod
    def exists(cls, name: str, start_path: Optional[Path] = None) -> bool:
        """
        Return True if a codemod with the given name exists.
        """
        return cls.get(name, start_path) is not None

    @classmethod
    def get_decorated(cls, start_path: Optional[Path] = None) -> builtins.list[DecoratedFunction]:
        """
        Alias for list(): return all codemod functions.
        """
        return cls.list(start_path)