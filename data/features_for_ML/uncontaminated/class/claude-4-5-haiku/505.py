from datetime import timedelta
from typing import Optional
import requests
from datetime import datetime


class RachioControllerHandler:
    """Handler for Rachio Controller devices."""

    def __init__(self, api_key: str, device_data: dict) -> None:
        self.api_key = api_key
        self.device_data = device_data
        self.device_id = device_data.get('id')
        self.zones = device_data.get('zones', [])
        self.last_update = datetime.now()
        self.status = device_data.get('status', 'ONLINE')
        self.name = device_data.get('name', '')
        self.model = device_data.get('model', '')
        self.serial_number = device_data.get('serialNumber', '')
        self.mac_address = device_data.get('macAddress', '')
        self.zone_states = {}
        self._initialize_zone_states()

    def _initialize_zone_states(self) -> None:
        """Initialize zone states from device data."""
        for zone in self.zones:
            zone_id = zone.get('id')
            self.zone_states[zone_id] = {
                'name': zone.get('name'),
                'number': zone.get('zoneNumber'),
                'enabled': zone.get('enabled', True),
                'duration': zone.get('duration', 0),
                'is_on': False,
                'remaining_time': 0
            }

    def get_zone_default_duration(self, zone_id: str) -> int:
        """Get the default duration for a zone in seconds."""
        for zone in self.zones:
            if zone.get('id') == zone_id:
                return zone.get('duration', 0)
        return 0

    def is_zone_optimistically_on(self, zone_id: str) -> bool:
        """Check if a zone is optimistically on (has remaining time)."""
        if zone_id in self.zone_states:
            return self.zone_states[zone_id]['is_on'] and self.zone_states[zone_id]['remaining_time'] > 0
        return False

    @staticmethod
    def calculate_safe_polling_interval(num_devices: int, target_max_calls_per_hour: int = 80) -> int:
        """Calculate safe polling interval in seconds based on number of devices."""
        if num_devices <= 0:
            return 60
        
        # Calculate calls per device per hour
        calls_per_device_per_hour = target_max_calls_per_hour / num_devices
        
        # Convert to seconds (3600 seconds in an hour)
        interval_seconds = 3600 / calls_per_device_per_hour
        
        # Ensure minimum interval of 30 seconds
        return max(30, int(interval_seconds))

    def _get_update_interval(self) -> timedelta:
        """Get the update interval for this controller."""
        # Default update interval is 60 seconds
        return timedelta(seconds=60)

    def _get_remaining_time(self) -> float:
        """Get remaining time for current zone operation in seconds."""
        current_time = datetime.now()
        elapsed = (current_time - self.last_update).total_seconds()
        
        # Find zone with remaining time
        for zone_id, zone_state in self.zone_states.items():
            if zone_state['is_on'] and zone_state['remaining_time'] > 0:
                remaining = zone_state['remaining_time'] - elapsed
                return max(0, remaining)
        
        return 0