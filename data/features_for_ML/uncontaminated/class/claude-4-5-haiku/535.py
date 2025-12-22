from typing import Dict, Any

class SummaryResults:

    def __init__(self):
        self.results = {}

    def to_json_dict(self) -> Dict[str, Any]:
        return self.results