import json
import urllib.request
import urllib.error


class CheckForUpdate:
    """
    This class will handle the update availability, useful for other scripts that use the sendemail,
    or for people that want to build their own update logic. Also can be used internally.
    """

    def __init__(self, current_version=None, update_url=None):
        """
        :param current_version: str, the current version of the software (e.g., "1.2.3")
        :param update_url: str, URL that returns JSON with the latest version info
        """
        self.current_version = current_version or "0.0.0"
        self.update_url = update_url or "https://example.com/latest.json"
        self._latest_info = None

    def _fetch_latest(self):
        try:
            with urllib.request.urlopen(self.update_url, timeout=5) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except (urllib.error.URLError, ValueError, json.JSONDecodeError):
            return None

    def _compare_versions(self, current, latest):
        def parse(v):
            return [int(part) for part in v.split(".") if part.isdigit()]

        try:
            return parse(latest) > parse(current)
        except Exception:
            return False

    def parse_as_resp(self):
        """
        Returns a dictionary with update information.
        Keys:
            - update_available (bool)
            - latest_version (str or None)
            - download_url (str or None)
            - error (str or None)
        """
        if self._latest_info is None:
            self._latest_info = self._fetch_latest()

        if not self._latest_info:
            return {
                "update_available": False,
                "latest_version": None,
                "download_url": None,
                "error": "Could not fetch update information",
            }

        latest_version = self._latest_info.get("version")
        download_url = self._latest_info.get("download_url")
        update_available = self._compare_versions(self.current_version, latest_version)

        return {
            "update_available": update_available,
            "latest_version": latest_version,
            "download_url": download_url,
            "error": None,
        }

    def parse_as_output(self):
        """
        Returns a human‑readable string describing the update status.
        """
        resp = self.parse_as_resp()

        if resp.get("error"):
            return f"Error: {resp['error']}"

        if resp["update_available"]:
            return (
                f"Update available: {resp['latest_version']} "
                f"(current: {self.current_version}). "
                f"Download at {resp['download_url']}"
            )
        else:
            return f"No update available. Current version {self.current_version} is up to date."