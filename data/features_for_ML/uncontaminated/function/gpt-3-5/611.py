from typing import Any

def get_anthropic_models() -> list[dict[str, Any]]:
    return [
        {"type": "model", "id": 1, "display_name": "Model 1", "created_at": "2022-01-01"},
        {"type": "model", "id": 2, "display_name": "Model 2", "created_at": "2022-02-01"},
        {"type": "model", "id": 3, "display_name": "Model 3", "created_at": "2022-03-01"}
    ]