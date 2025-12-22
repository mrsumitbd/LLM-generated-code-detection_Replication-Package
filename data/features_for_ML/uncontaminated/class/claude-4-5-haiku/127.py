from typing import get_origin, get_args, Union, Optional, List, Dict, Set, Tuple, Any
from dataclasses import Field, MISSING
import sys

class TypeConverter:
    """Converts Python type hints to Field objects"""

    @staticmethod
    def convert_type_hint(type_hint, default_value=None, has_default=False):
        try:
            return TypeConverter._convert_type_hint_unsafe(type_hint, default_value, has_default)
        except Exception:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata=None,
                kw_only=False,
            )

    @staticmethod
    def _convert_type_hint_unsafe(type_hint, default_value=None, has_default=False):
        origin = get_origin(type_hint)
        args = get_args(type_hint)
        
        # Handle None type
        if type_hint is type(None):
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata=None,
                kw_only=False,
            )
        
        # Handle Union types (including Optional)
        if origin is Union:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata={"union_args": args},
                kw_only=False,
            )
        
        # Handle List types
        if origin is list or origin is List:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata={"list_args": args},
                kw_only=False,
            )
        
        # Handle Dict types
        if origin is dict or origin is Dict:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata={"dict_args": args},
                kw_only=False,
            )
        
        # Handle Set types
        if origin is set or origin is Set:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata={"set_args": args},
                kw_only=False,
            )
        
        # Handle Tuple types
        if origin is tuple or origin is Tuple:
            return Field(
                default=default_value if has_default else MISSING,
                default_factory=MISSING,
                init=True,
                repr=True,
                hash=None,
                compare=True,
                metadata={"tuple_args": args},
                kw_only=False,
            )
        
        # Handle basic types
        return Field(
            default=default_value if has_default else MISSING,
            default_factory=MISSING,
            init=True,
            repr=True,
            hash=None,
            compare=True,
            metadata={"type": type_hint},
            kw_only=False,
        )