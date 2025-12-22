import requests
from typing import Dict, Any, Optional

class SOARClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def execute_playbook(self, playbook_id: int, params: Dict[str, Any]) -> Optional[str]:
        url = f"{self.base_url}/api/v1/playbooks/{playbook_id}/execute"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:
            return response.json().get("activity_id")
        return None

    def get_playbook_status(self, activity_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/activities/{activity_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_playbook_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/activities/{activity_id}/result"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def wait_for_completion(self, activity_id: str, interval: int = 5) -> Optional[Dict[str, Any]]:
        import time
        while True:
            status = self.get_playbook_status(activity_id)
            if status and status.get("status") in ["COMPLETED", "FAILED"]:
                return status
            time.sleep(interval)