from __future__ import annotations
from typing import Any, Dict, Optional


class TCL_SplitAC_Fresh_Air_DeviceData:
    """
    A lightweight container for a TCL Split AC Fresh Air device's state.
    It stores the device identifier, the current AWS IoT Thing state,
    and any delta updates that need to be applied.

    The class provides convenient accessors, a method to apply deltas
    (deep‑merge), and a simple representation for debugging.
    """

    def __init__(self, device_id: str, aws_thing_state: Dict[str, Any], delta: Dict[str, Any]) -> None:
        """
        Initialize the device data container.

        Parameters
        ----------
        device_id : str
            The unique identifier for the device.
        aws_thing_state : dict
            The current state of the device as reported by AWS IoT.
        delta : dict
            A dictionary containing state changes that need to be applied.
        """
        self._device_id: str = device_id
        self._state: Dict[str, Any] = dict(aws_thing_state)  # shallow copy to avoid side‑effects
        self._delta: Dict[str, Any] = dict(delta)

    # ------------------------------------------------------------------
    # Basic accessors
    # ------------------------------------------------------------------
    @property
    def device_id(self) -> str:
        """Return the device identifier."""
        return self._device_id

    @property
    def state(self) -> Dict[str, Any]:
        """Return the current state dictionary (read‑only)."""
        return dict(self._state)

    @property
    def delta(self) -> Dict[str, Any]:
        """Return the pending delta dictionary (read‑only)."""
        return dict(self._delta)

    # ------------------------------------------------------------------
    # State manipulation helpers
    # ------------------------------------------------------------------
    def get_state_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Return the value for *key* in the state, or *default* if missing."""
        return self._state.get(key, default)

    def set_state_value(self, key: str, value: Any) -> None:
        """Set the value for *key* in the state."""
        self._state[key] = value

    def apply_delta(self) -> None:
        """
        Apply the pending delta to the current state.

        The merge is performed recursively so that nested dictionaries
        are updated without discarding unrelated keys.
        """
        def _merge(target: Dict[str, Any], source: Dict[str, Any]) -> None:
            for k, v in source.items():
                if isinstance(v, dict) and isinstance(target.get(k), dict):
                    _merge(target[k], v)
                else:
                    target[k] = v

        _merge(self._state, self._delta)
        # Clear delta after applying
        self._delta.clear()

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable representation of the device data."""
        return {
            "device_id": self._device_id,
            "state": dict(self._state),
            "delta": dict(self._delta),
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(device_id={self._device_id!r}, "
            f"state={self._state!r}, delta={self._delta!r})"
        )