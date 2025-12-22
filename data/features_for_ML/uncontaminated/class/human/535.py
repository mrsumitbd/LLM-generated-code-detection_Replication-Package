from typing import Any, Dict, Optional
from dataclasses import asdict, dataclass

class SummaryResults:
    configuration: Dict[str, Any]
    total_completion_tokens: int = 0
    avg_completion_tokens: float = 0
    total_prompt_tokens: int = 0
    avg_prompt_tokens: float = 0
    accuracy: float = 0.0
    pass_at_k: Optional[Dict[str, float]] = None

    def to_json_dict(self) -> Dict[str, Any]:
        """Convert to a JSON-compatible dictionary."""
        return asdict(self)