import time
from __future__ import annotations
from typing import Optional, Dict, Any


class SeedEXState:
    """席德强化E释放的**当前**状态"""

    def __init__(self, cooldown: float = 10.0) -> None:
        """
        Parameters
        ----------
        cooldown : float, optional
            Cooldown time in seconds before the E skill can be used again.
        """
        self.cooldown: float = cooldown
        self._last_used: Optional[float] = None
        self._active: bool = False
        self._active_start: Optional[float] = None
        self._active_duration: Optional[float] = None

    def start(self, duration: float) -> None:
        """
        Activate the E skill for a given duration.

        Parameters
        ----------
        duration : float
            How long the skill should remain active in seconds.

        Raises
        ------
        RuntimeError
            If the skill is still on cooldown.
        """
        if not self.is_ready():
            raise RuntimeError("E skill is on cooldown")
        self._active = True
        self._active_start = time.time()
        self._active_duration = duration
        self._last_used = self._active_start

    def stop(self) -> None:
        """Deactivate the E skill."""
        self._active = False
        self._active_start = None
        self._active_duration = None

    def update(self) -> None:
        """Update internal state; should be called periodically."""
        if self._active and self._active_start is not None and self._active_duration is not None:
            elapsed = time.time() - self._active_start
            if elapsed >= self._active_duration:
                self.stop()

    def is_active(self) -> bool:
        """Return True if the skill is currently active."""
        return self._active

    def is_ready(self) -> bool:
        """Return True if the skill can be activated (cooldown elapsed)."""
        if self._last_used is None:
            return True
        return (time.time() - self._last_used) >= self.cooldown

    def time_until_ready(self) -> float:
        """Return the remaining cooldown time in seconds."""
        if self.is_ready():
            return 0.0
        return self.cooldown - (time.time() - self._last_used)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the state to a dictionary."""
        return {
            "cooldown": self.cooldown,
            "last_used": self._last_used,
            "active": self._active,
            "active_start": self._active_start,
            "active_duration": self._active_duration,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SeedEXState":
        """Create an instance from a dictionary."""
        obj = cls(cooldown=data.get("cooldown", 10.0))
        obj._last_used = data.get("last_used")
        obj._active = data.get("active", False)
        obj._active_start = data.get("active_start")
        obj._active_duration = data.get("active_duration")
        return obj

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(cooldown={self.cooldown}, "
            f"last_used={self._last_used}, active={self._active})"
        )