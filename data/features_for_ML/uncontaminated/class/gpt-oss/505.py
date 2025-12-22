from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class RachioControllerHandler:
    """Handler for Rachio Controller devices."""

    def __init__(self, api_key: str, device_data: Dict[str, Any]) -> None:
        """
        Initialize the handler with an API key and device data.

        Parameters
        ----------
        api_key : str
            The API key used to authenticate with the Rachio API.
        device_data : dict
            A dictionary containing device information, including zones and
            metadata such as the last update timestamp.
        """
        self.api_key = api_key
        self.device_data = device_data
        # Cache the list of zones for quick lookup
        self._zones: List[Dict[str, Any]] = device_data.get("zones", [])

    def get_zone_default_duration(self, zone_id: str) -> Optional[int]:
        """
        Return the default duration (in seconds) for a given zone.

        Parameters
        ----------
        zone_id : str
            The identifier of the zone.

        Returns
        -------
        int | None
            The default duration in seconds, or None if the zone is not found.
        """
        for zone in self._zones:
            if str(zone.get("id")) == str(zone_id):
                # Rachio API uses 'defaultDuration' in seconds
                return int(zone.get("defaultDuration", 0))
        return None

    def is_zone_optimistically_on(self, zone_id: str) -> bool:
        """
        Determine if a zone is currently running (optimistically).

        Parameters
        ----------
        zone_id : str
            The identifier of the zone.

        Returns
        -------
        bool
            True if the zone is running, False otherwise.
        """
        for zone in self._zones:
            if str(zone.get("id")) == str(zone_id):
                # Rachio API uses 'isRunning' boolean
                return bool(zone.get("isRunning", False))
        return False

    @staticmethod
    def calculate_safe_polling_interval(
        num_devices: int, target_max_calls_per_hour: int = 80
    ) -> int:
        """
        Calculate a safe polling interval (in seconds) to keep API calls
        below a target maximum per hour.

        Parameters
        ----------
        num_devices : int
            Number of devices that will be polled.
        target_max_calls_per_hour : int, optional
            Desired maximum number of API calls per hour. Default is 80.

        Returns
        -------
        int
            Polling interval in seconds.
        """
        if num_devices <= 0:
            return 3600  # default to 1 hour if no devices
        # Calls per hour = num_devices * 3600 / interval
        # Solve for interval: interval = num_devices * 3600 / target
        interval = (num_devices * 3600) / target_max_calls_per_hour
        # Ensure at least 1 second
        return max(1, int(round(interval)))

    def _get_update_interval(self) -> timedelta:
        """
        Determine the update interval for this controller based on the
        number of zones and a safe polling interval.

        Returns
        -------
        timedelta
            The interval between updates.
        """
        # Use the number of zones as a proxy for number of devices
        num_zones = len(self._zones)
        seconds = self.calculate_safe_polling_interval(num_zones)
        return timedelta(seconds=seconds)

    def _get_remaining_time(self) -> float:
        """
        Calculate the remaining time (in seconds) until the next update
        should occur.

        Returns
        -------
        float
            Seconds remaining until the next update. If the next update
            time has already passed, returns 0.0.
        """
        last_updated_str = self.device_data.get("lastUpdated")
        if not last_updated_str:
            # If we don't have a timestamp, assume we need to update immediately
            return 0.0

        try:
            last_updated = datetime.fromisoformat(last_updated_str)
        except ValueError:
            # Fallback: try parsing without timezone
            try:
                last_updated = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                return 0.0

        interval = self._get_update_interval()
        next_update = last_updated + interval
        now = datetime.utcnow()
        remaining = (next_update - now).total_seconds()
        return max(0.0, remaining)