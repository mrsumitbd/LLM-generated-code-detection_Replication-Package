import time
from typing import Dict, Any

class APIModule:
    """API security module (Refactored)"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.api_keys = {}
        self.rate_limits = {}

    def run(self) -> Dict[str, Any]:
        access_status = self._test_api_access()
        keys_status = self._test_api_keys()
        rate_status = self._test_rate_limiting()
        return {
            "access_status": access_status,
            "keys_status": keys_status,
            "rate_status": rate_status
        }

    def _test_api_access(self):
        try:
            self.scanner.check_api_access()
            return "Passed"
        except Exception:
            return "Failed"

    def _test_api_keys(self):
        try:
            self.scanner.check_api_keys(self.api_keys)
            return "Passed"
        except Exception:
            return "Failed"

    def _test_rate_limiting(self):
        try:
            self.scanner.check_rate_limiting(self.rate_limits)
            return "Passed"
        except Exception:
            return "Failed"