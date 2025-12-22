from typing import Optional

class BackgroundUpdateChecker:
    """Manages background checking for CLI updates."""

    def __init__(self, check_interval_hours: int = 24, cache_enabled: bool = True):
        self.check_interval_hours = check_interval_hours
        self.cache_enabled = cache_enabled

    def should_check(self) -> bool:
        pass

    def _save_cache(self, latest_version: Optional[str], update_available: bool) -> None:
        pass

    def _load_cached_result(self) -> Optional[str]:
        pass

    def _check_for_updates(self) -> None:
        pass

    def _format_update_message(self, current: str, latest: str) -> str:
        pass

    def _format_no_update_message(self, current: str, latest: str) -> str:
        pass

    def start_check(self) -> None:
        pass

    def get_result(self, timeout: float = 0.1) -> Optional[str]:
        pass