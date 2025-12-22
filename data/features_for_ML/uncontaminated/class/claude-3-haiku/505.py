import time
from datetime import datetime, timedelta

class RachioControllerHandler:
    """Handler for Rachio Controller devices."""

    def __init__(self, api_key: str, device_data: dict) -> None:
        self.api_key = api_key
        self.device_data = device_data
        self.last_update = datetime.now()

    def get_zone_default_duration(self, zone_id):
        for zone in self.device_data['zones']:
            if zone['id'] == zone_id:
                return zone['defaultDuration']
        return None

    def is_zone_optimistically_on(self, zone_id):
        for zone in self.device_data['zones']:
            if zone['id'] == zone_id:
                return zone['optimisticallyOn']
        return False

    @staticmethod
    def calculate_safe_polling_interval(num_devices: int, target_max_calls_per_hour: int = 80) -> int:
        calls_per_device_per_hour = target_max_calls_per_hour / num_devices
        return int(3600 / calls_per_device_per_hour)

    def _get_update_interval(self) -> timedelta:
        return self._get_remaining_time()

    def _get_remaining_time(self) -> float:
        time_since_last_update = datetime.now() - self.last_update
        return max(0, self.calculate_safe_polling_interval(1) - time_since_last_update.total_seconds())