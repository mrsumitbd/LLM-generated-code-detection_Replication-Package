import json as _json
import pickle as _pickle
import dataclasses as _dataclasses
from typing import Any, TypeVar, Type

T = TypeVar("T")

def deserialize(value: str | bytes, target_type: Type[T], json: bool = False) -> T:
    """
    Deserialize a value (JSON string/bytes or pickled bytes) into an instance of `target_type`.

    Parameters
    ----------
    value : str | bytes
        The serialized data. If `json` is True, this should be a JSON string or bytes.
        If `json` is False, this should be pickled bytes.
    target_type : type[T]
        The type to deserialize into. Can be a built‑in type, a dataclass, a NamedTuple,
        or any class that can be instantiated with keyword arguments.
    json : bool, default False
        If True, interpret `value` as JSON. If False, interpret `value` as pickled data.

    Returns
    -------
    T
        An instance of `target_type` constructed from the serialized data.
    """
    # Helper to instantiate target_type from a mapping
    def _from_mapping(mapping: Any) -> Any:
        if isinstance(mapping, dict):
            # Try dataclass
            if _dataclasses.is_dataclass(target_type):
                return target_type(**mapping)
            # Try NamedTuple or other class with **kwargs
            try:
                return target_type(**mapping)
            except TypeError:
                # Fallback: return mapping itself
                return mapping
        # If mapping is not a dict, just return it
        return mapping

    # If value is bytes and json flag is set, decode to str
    if isinstance(value, bytes):
        if json:
            try:
                value = value.decode("utf-8")
            except Exception:
                # If decoding fails, keep as bytes and let json.loads handle it
                pass

    # JSON deserialization
    if json:
        # Parse JSON
        parsed = _json.loads(value)
        # If target_type is a built-in simple type, cast directly
        if target_type in (int, float, str, bool):
            return target_type(parsed)  # type: ignore
        # If target_type is list or dict, return parsed directly
        if target_type in (list, dict):
            return parsed  # type: ignore
        # For other types, try to construct from mapping
        return _from_mapping(parsed)  # type: ignore

    # Pickle deserialization
    if isinstance(value, bytes):
        obj = _pickle.loads(value)
    else:
        # If value is a string but json=False, treat as pickled string representation
        # This is unlikely but we handle it gracefully
        obj = _pickle.loads(value.encode("utf-8"))

    # If target_type is a built-in simple type, cast directly
    if target_type in (int, float, str, bool):
        return target_type(obj)  # type: ignore
    # If target_type is list or dict, return obj directly
    if target_type in (list, dict):
        return obj  # type: ignore
    # If obj is already of target_type, return it
    if isinstance(obj, target_type):
        return obj
    # Try to construct target_type from obj if it's a mapping
    return _from_mapping(obj)  # type: ignore