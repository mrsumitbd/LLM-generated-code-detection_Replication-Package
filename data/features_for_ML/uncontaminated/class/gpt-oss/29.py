import requests
from typing import Any, Dict, Optional


class SessionManager:
    """Manages HTTP sessions with authentication"""

    def __init__(self, config: Any, auth_manager: Any):
        """
        Parameters
        ----------
        config : Any
            Configuration object that should expose at least:
            - base_url : str
            - headers : dict (optional)
            - timeout : float or tuple (optional)
        auth_manager : Any
            Authentication manager that should expose:
            - get_token() -> str | None
            - refresh_token() -> str | None
        """
        self.config = config
        self.auth_manager = auth_manager
        self.session = requests.Session()
        self._setup_session()

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _setup_session(self) -> None:
        """Initialise the session with headers, auth and timeout."""
        # Base headers
        headers: Dict[str, str] = getattr(self.config, "headers", {})
        self.session.headers.update(headers)

        # Auth header
        token = self.auth_manager.get_token()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        # Timeout
        timeout = getattr(self.config, "timeout", None)
        if timeout is not None:
            # requests.Session does not store timeout; we keep it for convenience
            self.session.timeout = timeout  # type: ignore[attr-defined]

    def _refresh_token(self) -> bool:
        """Refresh the authentication token and update the session header."""
        new_token = self.auth_manager.refresh_token()
        if new_token:
            self.session.headers.update({"Authorization": f"Bearer {new_token}"})
            return True
        return False

    def _build_url(self, url: str) -> str:
        """Build a full URL from a relative path."""
        if url.startswith(("http://", "https://")):
            return url
        base = getattr(self.config, "base_url", "")
        return f"{base.rstrip('/')}/{url.lstrip('/')}"

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def request(
        self,
        method: str,
        url: str,
        *,
        retry_on_401: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Send an HTTP request using the managed session.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, etc.).
        url : str
            Relative or absolute URL.
        retry_on_401 : bool, default True
            If True, automatically refresh the token and retry once on 401.
        **kwargs
            Additional arguments forwarded to ``requests.Session.request``.

        Returns
        -------
        requests.Response
        """
        full_url = self._build_url(url)
        response = self.session.request(method, full_url, **kwargs)

        if response.status_code == 401 and retry_on_401:
            if self._refresh_token():
                response = self.session.request(method, full_url, **kwargs)

        return response

    # Convenience wrappers
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("HEAD", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", url, **kwargs)

    # --------------------------------------------------------------------- #
    # Session access
    # --------------------------------------------------------------------- #
    @property
    def session_obj(self) -> requests.Session:
        """Return the underlying ``requests.Session`` instance."""
        return self.session