from __future__ import annotations

from typing import Dict, List, TypeVar

# Assume IPreprocessor is defined elsewhere in the codebase.
# For type checking purposes we can use a generic placeholder.
IPreprocessor = TypeVar("IPreprocessor")


class PreprocessorRegistry:
    _registry: Dict[str, IPreprocessor] = {}

    @staticmethod
    def register_preprocessor(preprocessor_id: str, preprocessor: IPreprocessor) -> None:
        """
        Register a preprocessor instance under the given identifier.

        If the identifier already exists, the existing entry is overwritten.
        """
        PreprocessorRegistry._registry[preprocessor_id] = preprocessor

    @staticmethod
    def get_preprocessor(preprocessor_id: str) -> IPreprocessor:
        """
        Retrieve the preprocessor registered under the given identifier.

        Raises:
            KeyError: If no preprocessor is registered with the given id.
        """
        try:
            return PreprocessorRegistry._registry[preprocessor_id]
        except KeyError as exc:
            raise KeyError(f"No preprocessor registered under id '{preprocessor_id}'.") from exc

    @staticmethod
    def get_preprocessor_ids() -> List[str]:
        """
        Return a list of all registered preprocessor identifiers.
        """
        return list(PreprocessorRegistry._registry.keys())