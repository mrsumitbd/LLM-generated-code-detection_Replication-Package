from typing import Dict, Any

class SummaryResults:
    def __init__(self, total_count: int, successful_count: int, failed_count: int, error_messages: Dict[str, str]):
        self.total_count = total_count
        self.successful_count = successful_count
        self.failed_count = failed_count
        self.error_messages = error_messages

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "total_count": self.total_count,
            "successful_count": self.successful_count,
            "failed_count": self.failed_count,
            "error_messages": self.error_messages
        }