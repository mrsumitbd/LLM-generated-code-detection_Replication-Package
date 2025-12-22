from typing import Dict, Any, List, Tuple, Optional
import time
import random


class APIModule:
    """API security module (Refactored)"""

    def __init__(self, scanner):
        """
        Initialize the API security module with a scanner object.

        :param scanner: An object that provides API endpoint information and
                        methods to interact with the API for testing.
        """
        self.scanner = scanner
        self.results: Dict[str, Any] = {}

    def run(self) -> Dict[str, Any]:
        """
        Execute all API security tests and return a dictionary of results.

        :return: Dictionary containing the results of each test.
        """
        self.results["access"] = self._test_api_access()
        self.results["keys"] = self._test_api_keys()
        self.results["rate_limiting"] = self._test_rate_limiting()
        return self.results

    def _test_api_access(self) -> Dict[str, Any]:
        """
        Test whether the API endpoints are accessible and return expected status codes.

        :return: Dictionary with endpoint URLs as keys and a tuple of (status_code, success) as values.
        """
        access_results: Dict[str, Tuple[int, bool]] = {}
        endpoints: List[str] = getattr(self.scanner, "endpoints", [])
        for url in endpoints:
            try:
                status = self.scanner.get_status(url)
                success = status == 200
            except Exception:
                status = None
                success = False
            access_results[url] = (status, success)
        return access_results

    def _test_api_keys(self) -> Dict[str, Any]:
        """
        Test whether API keys are required and correctly validated.

        :return: Dictionary with key names as keys and a boolean indicating validity.
        """
        key_results: Dict[str, bool] = {}
        keys: List[Tuple[str, str]] = getattr(self.scanner, "api_keys", [])
        for key_name, key_value in keys:
            try:
                valid = self.scanner.validate_key(key_value)
            except Exception:
                valid = False
            key_results[key_name] = valid
        return key_results

    def _test_rate_limiting(self) -> Dict[str, Any]:
        """
        Test whether the API enforces rate limiting.

        :return: Dictionary with endpoint URLs as keys and a boolean indicating if rate limiting was observed.
        """
        rate_results: Dict[str, bool] = {}
        endpoints: List[str] = getattr(self.scanner, "endpoints", [])
        for url in endpoints:
            try:
                # Send a burst of requests
                responses = []
                for _ in range(10):
                    responses.append(self.scanner.get_status(url))
                    time.sleep(0.05)  # small delay between requests
                # If any response is 429, rate limiting is in effect
                rate_limited = any(r == 429 for r in responses)
            except Exception:
                rate_limited = False
            rate_results[url] = rate_limited
        return rate_results