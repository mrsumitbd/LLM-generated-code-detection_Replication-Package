from typing import Dict, Any, List, Optional


class PluginBruteforceModule:
    """Plugin discovery via bruteforce (Refactored)"""

    def __init__(self, scanner):
        """
        Initialize the module with a scanner object.

        The scanner is expected to provide:
            - base_url: the target base URL as a string.
            - A request method (either `get` or `request`) that accepts a URL
              and returns an object with a `status_code` attribute.
        """
        self.scanner = scanner
        self.discovered: List[str] = []

    def run(self) -> Dict[str, Any]:
        """
        Execute the bruteforce discovery process.

        Returns:
            A dictionary containing the list of discovered plugin URLs.
        """
        self._bruteforce_plugins()
        return {"plugins": self.discovered}

    def _bruteforce_plugins(self):
        """
        Perform a simple bruteforce against a list of common plugin paths.

        The method attempts to fetch each path and records the URL if the
        response status code is 200. Errors are silently ignored.
        """
        # Common plugin / admin / API paths that are often present on web apps
        common_paths = [
            "/wp-admin/admin-ajax.php",
            "/wp-content/plugins/",
            "/wp-content/themes/",
            "/wp-includes/",
            "/wp-login.php",
            "/wp-config.php",
            "/.git/",
            "/.svn/",
            "/.env",
            "/config.php",
            "/admin/",
            "/administrator/",
            "/admin/login.php",
            "/admin.php",
            "/login.php",
            "/user/login",
            "/user/login.php",
            "/api/",
            "/api/v1/",
            "/api/v2/",
            "/api/v3/",
            "/api/v4/",
            "/api/v5/",
            "/api/v6/",
            "/api/v7/",
            "/api/v8/",
            "/api/v9/",
            "/api/v10/",
            "/api/v11/",
            "/api/v12/",
            "/api/v13/",
            "/api/v14/",
            "/api/v15/",
            "/api/v16/",
            "/api/v17/",
            "/api/v18/",
            "/api/v19/",
            "/api/v20/",
            "/api/v21/",
            "/api/v22/",
            "/api/v23/",
            "/api/v24/",
            "/api/v25/",
            "/api/v26/",
            "/api/v27/",
            "/api/v28/",
            "/api/v29/",
            "/api/v30/",
            "/api/v31/",
            "/api/v32/",
            "/api/v33/",
            "/api/v34/",
            "/api/v35/",
            "/api/v36/",
            "/api/v37/",
            "/api/v38/",
            "/api/v39/",
            "/api/v40/",
            "/api/v41/",
            "/api/v42/",
            "/api/v43/",
            "/api/v44/",
            "/api/v45/",
            "/api/v46/",
            "/api/v47/",
            "/api/v48/",
            "/api/v49/",
            "/api/v50/",
        ]

        # Helper to perform a GET request using the scanner
        def _request(url: str) -> Optional[Any]:
            # Prefer a `get` method if available
            if hasattr(self.scanner, "get"):
                return self.scanner.get(url)
            # Fallback to a generic `request` method
            if hasattr(self.scanner, "request"):
                return self.scanner.request(url)
            return None

        base = getattr(self.scanner, "base_url", "").rstrip("/")
        for path in common_paths:
            try:
                url = f"{base}{path}"
                resp = _request(url)
                if resp and getattr(resp, "status_code", None) == 200:
                    self.discovered.append(url)
            except Exception:
                # Ignore any errors (network, timeout, etc.)
                continue