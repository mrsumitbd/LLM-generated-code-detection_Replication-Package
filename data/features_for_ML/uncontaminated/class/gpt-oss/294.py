from typing import Any, Dict, Optional


class VirtualFilter:
    """Virtual filter device - 完全按照 Filter.action 规范 🌊"""

    def __init__(
        self,
        device_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        # Basic identification
        self.device_id = device_id or kwargs.get("device_id")

        # Default configuration
        cfg: Dict[str, Any] = config or {}

        # Internal state variables
        self._status: str = cfg.get("status", "idle")
        self._progress: float = cfg.get("progress", 0.0)
        self._current_temp: float = cfg.get("current_temp", 25.0)
        self._current_status: str = cfg.get("current_status", "stopped")
        self._filtered_volume: float = cfg.get("filtered_volume", 0.0)
        self._message: str = cfg.get("message", "")

        # Maximum limits
        self._max_temp: float = cfg.get("max_temp", 100.0)
        self._max_stir_speed: float = cfg.get("max_stir_speed", 2000.0)
        self._max_volume: float = cfg.get("max_volume", 1000.0)

    @property
    def status(self) -> str:
        """Overall status of the filter device."""
        return self._status

    @property
    def progress(self) -> float:
        """Progress of the current filtering operation (0.0–1.0)."""
        return self._progress

    @property
    def current_temp(self) -> float:
        """Current temperature of the filter (°C)."""
        return self._current_temp

    @property
    def current_status(self) -> str:
        """Current operational status (e.g., 'running', 'paused')."""
        return self._current_status

    @property
    def filtered_volume(self) -> float:
        """Total volume filtered so far (liters)."""
        return self._filtered_volume

    @property
    def message(self) -> str:
        """Human‑readable message or error description."""
        return self._message

    @property
    def max_temp(self) -> float:
        """Maximum allowable temperature (°C)."""
        return self._max_temp

    @property
    def max_stir_speed(self) -> float:
        """Maximum stirring speed (rpm)."""
        return self._max_stir_speed

    @property
    def max_volume(self) -> float:
        """Maximum filterable volume (liters)."""
        return self._max_volume