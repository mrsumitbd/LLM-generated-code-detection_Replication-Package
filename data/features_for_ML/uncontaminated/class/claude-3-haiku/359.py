import requests
from typing import Dict, Any, Optional

class AdminPanelModule:
    """Admin panel security testing"""

    def __init__(self, target_url: str, session: Optional[Any] = None, verbose: bool = False):
        self.target_url = target_url
        self.session = session or requests.Session()
        self.verbose = verbose

    def scan(self) -> Dict[str, Any]:
        result = {}
        try:
            response = self.session.get(self.target_url)
            if response.status_code == 200:
                if "/admin" in response.text or "/dashboard" in response.text:
                    result["admin_panel_found"] = True
                else:
                    result["admin_panel_found"] = False
            else:
                result["admin_panel_found"] = False
        except requests.exceptions.RequestException as e:
            result["error"] = str(e)
            result["admin_panel_found"] = False

        if self.verbose:
            print(result)

        return result