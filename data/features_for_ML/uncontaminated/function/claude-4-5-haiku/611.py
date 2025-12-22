import anthropic
from typing import Any


def get_anthropic_models() -> list[dict[str, Any]]:
    """Get list of Anthropic models with metadata.

    Returns:
        List of Anthropic model entries with type, id, display_name, and created_at fields
    """
    client = anthropic.Anthropic()
    response = client.models.list()
    
    models = []
    for model in response.data:
        model_dict = {
            "type": model.type,
            "id": model.id,
            "display_name": model.display_name,
            "created_at": model.created_at
        }
        models.append(model_dict)
    
    return models