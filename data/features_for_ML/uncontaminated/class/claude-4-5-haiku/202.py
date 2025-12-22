from typing import Dict, Any, Optional
import time
import requests
from requests.auth import HTTPBasicAuth
import os

class SOARClient:

    def __init__(self):
        self.base_url = os.getenv('SOAR_BASE_URL', 'http://localhost:8080')
        self.username = os.getenv('SOAR_USERNAME', 'admin')
        self.password = os.getenv('SOAR_PASSWORD', 'admin')
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self.session.headers.update({'Content-Type': 'application/json'})

    def execute_playbook(self, playbook_id: int, params: Dict[str, Any]) -> Optional[str]:
        try:
            url = f"{self.base_url}/api/v2/playbooks/{playbook_id}/execute"
            response = self.session.post(url, json=params)
            response.raise_for_status()
            data = response.json()
            return data.get('activity_id') or data.get('id')
        except Exception as e:
            print(f"Error executing playbook: {e}")
            return None

    def get_playbook_status(self, activity_id: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/api/v2/activities/{activity_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting playbook status: {e}")
            return None

    def get_playbook_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/api/v2/activities/{activity_id}/result"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting playbook result: {e}")
            return None

    def wait_for_completion(self, activity_id: str, interval: int = 5) -> Optional[Dict[str, Any]]:
        try:
            max_attempts = 1200
            attempts = 0
            
            while attempts < max_attempts:
                status = self.get_playbook_status(activity_id)
                
                if status is None:
                    return None
                
                state = status.get('state') or status.get('status')
                
                if state in ['COMPLETED', 'FAILED', 'CANCELLED', 'completed', 'failed', 'cancelled']:
                    return self.get_playbook_result(activity_id)
                
                time.sleep(interval)
                attempts += 1
            
            print(f"Timeout waiting for activity {activity_id} to complete")
            return None
        except Exception as e:
            print(f"Error waiting for completion: {e}")
            return None