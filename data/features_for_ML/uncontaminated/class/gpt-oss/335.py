import os
import json
import time
import threading
import queue
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from packaging.version import Version


class BackgroundUpdateChecker:
    """Manages background checking for CLI updates."""

    _CACHE_FILE = Path.home() / ".cli_update_cache.json"

    def __init__(self, check_interval_hours: int = 24, cache_enabled: bool = True):
        self.check_interval = timedelta(hours=check_interval_hours)
        self.cache_enabled = cache_enabled
        self._last_check: Optional[datetime] = None
        self._result_queue: queue.Queue[str] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def should_check(self) -> bool:
        if not self.cache_enabled:
            return True
        if self._last_check is None:
            return True
        return datetime.utcnow() - self._last_check >= self.check_interval

    def _save_cache(self, latest_version: Optional[Version], update_available: bool) -> None:
        if not self.cache_enabled:
            return
        data = {
            "latest_version": str(latest_version) if latest_version else None,
            "update_available": update_available,
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            with self._CACHE_FILE.open("w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass  # ignore cache write errors

    def _load_cached_result(self) -> Optional[str]:
        if not self.cache_enabled:
            return None
        if not self._CACHE_FILE.exists():
            return None
        try:
            with self._CACHE_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            latest = data.get("latest_version")
            update_available = data.get("update_available", False)
            if latest is None:
                return None
            current = self._current_version()
            if update_available:
                return self._format_update_message(current, latest)
            else:
                return self._format_no_update_message(current, latest)
        except Exception:
            return None

    def _check_for_updates(self) -> None:
        try:
            current = self._current_version()
            latest = self._fetch_latest_version()
            update_available = False
            if latest and Version(latest) > current:
                update_available = True
                message = self._format_update_message(str(current), latest)
            else:
                message = self._format_no_update_message(str(current), str(latest))
            self._save_cache(Version(latest) if latest else None, update_available)
            self._result_queue.put(message)
        finally:
            self._last_check = datetime.utcnow()

    def _format_update_message(self, current: str, latest: str) -> str:
        return f"Update available: {current} → {latest}"

    def _format_no_update_message(self, current: str, latest: str) -> str:
        return f"You are up to date: {current} (latest {latest})"

    def start_check(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        if not self.should_check():
            # Load cached result if available
            cached = self._load_cached_result()
            if cached:
                self._result_queue.put(cached)
            return

        def target():
            while not self._stop_event.is_set():
                self._check_for_updates()
                break

        self._thread = threading.Thread(target=target, daemon=True)
        self._thread.start()

    def get_result(self, timeout: float = 0.1) -> Optional[str]:
        try:
            return self._result_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    # ------------------------------------------------------------------
    # Helper methods (can be overridden or monkey‑patched in tests)
    # ------------------------------------------------------------------
    def _current_version(self) -> Version:
        """Return the current CLI version. Override in tests if needed."""
        # Default placeholder; replace with actual version retrieval logic.
        return Version("0.0.0")

    def _fetch_latest_version(self) -> Optional[str]:
        """Fetch the latest version string from the update source."""
        # Placeholder implementation; replace with real network call if desired.
        # For example, read from a URL or package index.
        return "1.0.0"