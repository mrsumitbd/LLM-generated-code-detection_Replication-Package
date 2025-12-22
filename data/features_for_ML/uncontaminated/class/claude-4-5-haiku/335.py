import json
import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from packaging.version import Version


class BackgroundUpdateChecker:
    """Manages background checking for CLI updates."""

    def __init__(self, check_interval_hours: int = 24, cache_enabled: bool = True):
        self.check_interval_hours = check_interval_hours
        self.cache_enabled = cache_enabled
        self.cache_dir = Path.home() / ".cache" / "cli_update_checker"
        self.cache_file = self.cache_dir / "update_check.json"
        self._check_thread: Optional[threading.Thread] = None
        self._result: Optional[str] = None
        self._result_lock = threading.Lock()
        self._current_version = "1.0.0"
        self._latest_version: Optional[Version] = None

    def should_check(self) -> bool:
        if not self.cache_enabled:
            return True

        if not self.cache_file.exists():
            return True

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                last_check = datetime.fromisoformat(data.get("last_check", ""))
                return datetime.now() - last_check > timedelta(hours=self.check_interval_hours)
        except (json.JSONDecodeError, ValueError, KeyError):
            return True

    def _save_cache(self, latest_version: Optional[Version], update_available: bool) -> None:
        if not self.cache_enabled:
            return

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        cache_data = {
            "last_check": datetime.now().isoformat(),
            "latest_version": str(latest_version) if latest_version else None,
            "update_available": update_available,
        }

        try:
            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f)
        except (IOError, OSError):
            pass

    def _load_cached_result(self) -> Optional[str]:
        if not self.cache_enabled or not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                if data.get("update_available"):
                    current = self._current_version
                    latest = data.get("latest_version", "")
                    return self._format_update_message(current, latest)
                else:
                    current = self._current_version
                    latest = data.get("latest_version", current)
                    return self._format_no_update_message(current, latest)
        except (json.JSONDecodeError, IOError, OSError):
            return None

    def _check_for_updates(self) -> None:
        try:
            current_version = Version(self._current_version)
            self._latest_version = Version("1.0.1")

            update_available = self._latest_version > current_version

            self._save_cache(self._latest_version, update_available)

            with self._result_lock:
                if update_available:
                    self._result = self._format_update_message(
                        str(current_version), str(self._latest_version)
                    )
                else:
                    self._result = self._format_no_update_message(
                        str(current_version), str(self._latest_version)
                    )
        except Exception:
            pass

    def _format_update_message(self, current: str, latest: str) -> str:
        return f"Update available: {current} → {latest}"

    def _format_no_update_message(self, current: str, latest: str) -> str:
        return f"You are on the latest version: {current}"

    def start_check(self) -> None:
        if self.should_check():
            self._check_thread = threading.Thread(target=self._check_for_updates, daemon=True)
            self._check_thread.start()
        else:
            cached_result = self._load_cached_result()
            with self._result_lock:
                self._result = cached_result

    def get_result(self, timeout: float = 0.1) -> Optional[str]:
        if self._check_thread:
            self._check_thread.join(timeout=timeout)

        with self._result_lock:
            return self._result