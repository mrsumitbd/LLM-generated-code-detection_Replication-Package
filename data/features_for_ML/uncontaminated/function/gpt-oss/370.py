import json
import sys
from pprint import pformat
from typing import Any

def dump_state(state: Any, label: str = "Current Execution State") -> None:
    """
    Helper method to dump the current state for debugging.

    The function attempts to produce a readable representation of the
    supplied `state`.  It handles dictionaries, lists, tuples, sets,
    objects with a ``__dict__`` attribute, and objects with ``__slots__``.
    If the state cannot be serialized to JSON, a fallback pretty‑print
    representation is used.

    Args:
        state: Execution state to dump.
        label: Optional label for the state dump.
    """
    def _to_dict(obj: Any) -> Any:
        """Recursively convert an object to a serializable structure."""
        if isinstance(obj, (dict, list, tuple, set)):
            return type(obj)(_to_dict(v) for v in obj)
        if hasattr(obj, "__dict__"):
            return {k: _to_dict(v) for k, v in obj.__dict__.items()}
        if hasattr(obj, "__slots__"):
            return {slot: _to_dict(getattr(obj, slot)) for slot in obj.__slots__}
        # Fallback: use string representation
        return repr(obj)

    try:
        serializable = _to_dict(state)
        dump = json.dumps(serializable, indent=2, default=str, sort_keys=True)
    except Exception:
        # If JSON serialization fails, fall back to pretty print
        dump = pformat(state, width=80, compact=False)

    output = f"{label}:\n{dump}"
    print(output, file=sys.stdout)