from typing import Dict, Any, Optional

class SOARClient:

    def __init__(self):
        pass

    def execute_playbook(self, playbook_id: int, params: Dict[str, Any]) -> Optional[str]:
        pass

    def get_playbook_status(self, activity_id: str) -> Optional[Dict[str, Any]]:
        pass

    def get_playbook_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        pass

    def wait_for_completion(self, activity_id: str, interval: int = 5) -> Optional[Dict[str, Any]]:
        pass