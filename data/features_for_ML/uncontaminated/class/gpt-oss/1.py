from typing import Any, Dict, Optional
import requests
import json


class WebhookSecurityModule:
    """Webhook security testing"""

    def __init__(self, target_url: str, session: Optional[Any] = None, verbose: bool = False):
        """
        Initialize the WebhookSecurityModule.

        :param target_url: The webhook endpoint to test.
        :param session: Optional requests-like session object. If None, a new Session is created.
        :param verbose: If True, prints detailed debug information.
        """
        self.target_url = target_url.rstrip("/")
        self.session = session or requests.Session()
        self.verbose = verbose

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def _request(self, method: str, **kwargs) -> requests.Response:
        """
        Helper to perform a request with the configured session.
        """
        self._log(f"Sending {method} request to {self.target_url} with kwargs: {kwargs}")
        return self.session.request(method, self.target_url, **kwargs)

    def scan(self) -> Dict[str, Any]:
        """
        Perform a basic security scan on the webhook endpoint.

        The scan includes:
            - Checking if the endpoint requires authentication (401/403).
            - Testing if the endpoint accepts arbitrary JSON payloads.
            - Checking for common HTTP status codes and headers.

        :return: A dictionary containing scan results.
        """
        results: Dict[str, Any] = {
            "target_url": self.target_url,
            "requires_auth": None,
            "accepts_json": None,
            "status_codes": {},
            "headers": {},
            "response_body": None,
        }

        # 1. Test GET request
        try:
            get_resp = self._request("GET")
            results["status_codes"]["GET"] = get_resp.status_code
            results["headers"]["GET"] = dict(get_resp.headers)
            if get_resp.status_code in (401, 403):
                results["requires_auth"] = True
            else:
                results["requires_auth"] = False
        except Exception as e:
            self._log(f"GET request failed: {e}")
            results["status_codes"]["GET"] = "error"
            results["requires_auth"] = True

        # 2. Test POST request with empty JSON payload
        try:
            post_resp = self._request(
                "POST",
                json={},
                headers={"Content-Type": "application/json"},
            )
            results["status_codes"]["POST_empty"] = post_resp.status_code
            results["headers"]["POST_empty"] = dict(post_resp.headers)
            if post_resp.status_code in (200, 201, 202, 204):
                results["accepts_json"] = True
            else:
                results["accepts_json"] = False
        except Exception as e:
            self._log(f"POST empty request failed: {e}")
            results["status_codes"]["POST_empty"] = "error"
            results["accepts_json"] = False

        # 3. Test POST request with arbitrary payload
        try:
            payload = {"test": "data", "number": 123, "nested": {"a": 1}}
            post_resp = self._request(
                "POST",
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            results["status_codes"]["POST_payload"] = post_resp.status_code
            results["headers"]["POST_payload"] = dict(post_resp.headers)
            results["response_body"] = post_resp.text
        except Exception as e:
            self._log(f"POST payload request failed: {e}")
            results["status_codes"]["POST_payload"] = "error"
            results["response_body"] = None

        return results