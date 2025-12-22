import requests
from typing import Any

def get_anthropic_models() -> list[dict[str, Any]]:
    """Get list of Anthropic models with metadata.

    Returns:
        List of Anthropic model entries with type, id, display_name, and created_at fields
    """
    url = "https://api.anthropic.com/v1/models"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "type": model["type"],
            "id": model["id"],
            "display_name": model["display_name"],
            "created_at": model["created_at"]
        }
        for model in data["models"]
    ]