import os
import re
from pathlib import Path
from typing import Callable, List, Optional

from .decorators import DecoratedFunction

class CodemodManager:
    """Manages codemod operations in the local filesystem."""

    @staticmethod
    def get_valid_name(name: str) -> str:
        """
        Returns a valid name for a codemod, based on the provided name.
        The valid name is a sanitized version of the input name, with
        non-alphanumeric characters replaced with underscores.
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', name)

    @classmethod
    def get_codemod(cls, name: str, start_path: Optional[Path] = None) -> DecoratedFunction:
        """
        Retrieves a codemod function by its name.
        If a start_path is provided, the search is limited to that directory and its subdirectories.
        """
        codemod = cls.get(name, start_path)
        if codemod is None:
            raise ValueError(f"Codemod '{name}' not found.")
        return codemod

    @classmethod
    def list(cls, start_path: Optional[Path] = None) -> List[DecoratedFunction]:
        """
        Returns a list of all available codemod functions.
        If a start_path is provided, the search is limited to that directory and its subdirectories.
        """
        return cls.get_decorated(start_path)

    @classmethod
    def get(cls, name: str, start_path: Optional[Path] = None) -> Optional[DecoratedFunction]:
        """
        Retrieves a codemod function by its name.
        If a start_path is provided, the search is limited to that directory and its subdirectories.
        Returns None if the codemod is not found.
        """
        for codemod in cls.get_decorated(start_path):
            if codemod.__name__ == name:
                return codemod
        return None

    @classmethod
    def exists(cls, name: str, start_path: Optional[Path] = None) -> bool:
        """
        Checks if a codemod function with the given name exists.
        If a start_path is provided, the search is limited to that directory and its subdirectories.
        """
        return cls.get(name, start_path) is not None

    @classmethod
    def get_decorated(cls, start_path: Optional[Path] = None) -> List[DecoratedFunction]:
        """
        Returns a list of all codemod functions that have been decorated with the `@codemod` decorator.
        If a start_path is provided, the search is limited to that directory and its subdirectories.
        """
        codemods = []
        if start_path is None:
            start_path = Path.cwd()
        for root, _, files in os.walk(start_path):
            for file in files:
                if file.endswith('.py'):
                    module_path = os.path.join(root, file[:-3])
                    module_path = module_path.replace(os.path.sep, '.')
                    module = __import__(module_path, fromlist=[''])
                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, DecoratedFunction):
                            codemods.append(obj)
        return codemods