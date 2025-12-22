import os
import time
from typing import Any, Dict, Optional

import requests
from requests import Session, Response


class SOARClient:
    """
    A minimal client for interacting with a SOAR platform.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> None:
        """
        Initialize the client.

        Parameters
        ----------
        base_url : str, optional
            Base URL of the SOAR API. Defaults to the value of the
            ``SOAR_BASE_URL`` environment variable or
            ``https://api.soar.example.com``.
        token : str, optional
            Bearer token for authentication. Defaults to the value of the
            ``SOAR_TOKEN`` environment variable.
        session : requests.Session, optional
            Custom session to use. If not provided, a new session is created.
        """
        self.base_url = base_url or os.getenv("SOAR_BASE_URL", "https://api.soar.example.com")
        self.token = token or os.getenv("SOAR_TOKEN")
        self.session = session or requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Response]:
        """
        Internal helper to perform an HTTP request.

        Returns the Response object if the request succeeds (status code 2xx),
        otherwise returns None.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            resp = self.session.request(method, url, timeout=30, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.RequestException:
            return None

    def execute_playbook(self, playbook_id: int, params: Dict[str, Any]) -> Optional[str]:
        """
        Execute a playbook.

        Returns the activity ID if the request succeeds, otherwise None.
        """
        endpoint = f"playbooks/{playbook_id}/execute"
        resp = self._request("POST", endpoint, json=params)
        if resp is None:
            return None
        data = resp.json()
        return data.get("activity_id")

    def get_playbook_status(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the status of a playbook activity.

        Returns a dictionary containing status information, or None on failure.
        """
        endpoint = f"playbooks/activity/{activity_id}/status"
        resp = self._request("GET", endpoint)
        if resp is None:
            return None
        return resp.json()

    def get_playbook_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the result of a completed playbook activity.

        Returns a dictionary containing the result, or None on failure.
        """
        endpoint = f"playbooks/activity/{activity_id}/result"
        resp = self._request("GET", endpoint)
        if resp is None:
            return None
        return resp.json()

    def wait_for_completion(self, activity_id: str, interval: int = 5) -> Optional[Dict[str, Any]]:
        """
        Poll the playbook status until it is completed or failed.

        Returns the final result dictionary if the activity completes successfully,
        otherwise returns None.
        """
        while True:
            status = self.get_playbook_status(activity_id)
            if status is None:
                return None

            state = status.get("state")
            if state in ("completed", "succeeded"):
                return self.get_playbook_result(activity_id)
            if state in ("failed", "error"):
                return None

            time.sleep(interval)