from typing import Any, Dict, Optional
import requests
import re


class AdminPanelModule:
    """Admin panel security testing"""

    # Common admin panel paths to test
    _COMMON_PATHS = [
        "/admin",
        "/admin/",
        "/admin/login",
        "/admin/login.php",
        "/admin.php",
        "/administrator",
        "/administrator/",
        "/administrator/login",
        "/admin_area",
        "/admin_area/login",
        "/adminpanel",
        "/adminpanel/login",
        "/cpanel",
        "/cpanel/login",
        "/panel",
        "/panel/login",
        "/backend",
        "/backend/login",
    ]

    def __init__(self, target_url: str, session: Optional[Any] = None, verbose: bool = False):
        """
        :param target_url: Base URL of the target (e.g., "https://example.com")
        :param session: Optional requests.Session or similar object
        :param verbose: If True, print progress information
        """
        self.target_url = target_url.rstrip("/")
        self.session = session or requests.Session()
        self.verbose = verbose

    def _request(self, path: str) -> Optional[requests.Response]:
        """Send a GET request to the target URL + path."""
        url = f"{self.target_url}{path}"
        try:
            resp = self.session.get(url, timeout=10, allow_redirects=True, verify=False)
            return resp
        except Exception as e:
            if self.verbose:
                print(f"[!] Error requesting {url}: {e}")
            return None

    def _is_admin_page(self, resp: requests.Response) -> bool:
        """Heuristically determine if a response looks like an admin page."""
        if resp is None:
            return False
        # Check status code
        if resp.status_code != 200:
            return False
        # Check for common admin keywords in content
        content = resp.text.lower()
        keywords = [
            "admin",
            "login",
            "username",
            "password",
            "dashboard",
            "control panel",
            "cpanel",
            "backend",
        ]
        return any(k in content for k in keywords)

    def scan(self) -> Dict[str, Any]:
        """
        Scan the target for common admin panel URLs.

        :return: Dictionary mapping each tested path to a dict containing:
                 - status: HTTP status code or None
                 - found: bool indicating if an admin page was detected
                 - url: full URL tested
        """
        results: Dict[str, Any] = {}
        for path in self._COMMON_PATHS:
            if self.verbose:
                print(f"[+] Testing {path}")
            resp = self._request(path)
            status = resp.status_code if resp else None
            found = self._is_admin_page(resp)
            results[path] = {
                "url": f"{self.target_url}{path}",
                "status": status,
                "found": found,
            }
            if self.verbose and found:
                print(f"[+] Admin panel found at {self.target_url}{path} (status {status})")
        return results