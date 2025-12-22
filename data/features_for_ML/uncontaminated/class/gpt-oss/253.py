from __future__ import annotations

import os
from typing import Dict, Optional


class AsyncAgentApiClient:
    """Async client for interacting with the Automagik Agents API."""

    def __init__(self, config_override: Optional[Dict[str, str]] = None):
        """
        Initialize the client.

        Parameters
        ----------
        config_override : Optional[Dict[str, str]]
            Optional dictionary to override default configuration.
            Supported keys:
                - base_url: Base URL of the API.
                - token: Bearer token for authentication.
                - headers: Default headers to include in every request.
        """
        # Default configuration
        self.base_url: str = os.getenv("AGENT_API_BASE_URL", "http://localhost:8000")
        self.token: Optional[str] = os.getenv("AGENT_API_TOKEN")
        self.default_headers: Dict[str, str] = {}

        # Apply overrides if provided
        if config_override:
            if "base_url" in config_override:
                self.base_url = config_override["base_url"]
            if "token" in config_override:
                self.token = config_override["token"]
            if "headers" in config_override:
                # Merge provided headers with defaults
                self.default_headers.update(config_override["headers"])

    def _make_headers(self, accept_sse: bool = False) -> Dict[str, str]:
        """
        Construct HTTP headers for a request.

        Parameters
        ----------
        accept_sse : bool, optional
            If True, set the Accept header to 'text/event-stream' to
            indicate a Server-Sent Events (SSE) stream. Defaults to False.

        Returns
        -------
        Dict[str, str]
            Dictionary of HTTP headers.
        """
        headers: Dict[str, str] = dict(self.default_headers)

        # Accept header
        headers["Accept"] = "text/event-stream" if accept_sse else "application/json"

        # Content-Type for JSON payloads
        headers.setdefault("Content-Type", "application/json")

        # Authorization header if token is available
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers