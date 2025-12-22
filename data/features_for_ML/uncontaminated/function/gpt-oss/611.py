from __future__ import annotations

from typing import Any, List, Dict

try:
    # The anthropic library is optional; import lazily
    from anthropic import Anthropic
except Exception:  # pragma: no cover
    Anthropic = None  # type: ignore


def get_anthropic_models() -> List[Dict[str, Any]]:
    """
    Get list of Anthropic models with metadata.

    Returns:
        List of Anthropic model entries with type, id, display_name, and created_at fields
    """
    if Anthropic is None:
        # If the anthropic library is not available, return an empty list
        return []

    try:
        client = Anthropic()
        # The API returns a list of model objects
        raw_models = client.list_models()
    except Exception:
        # If any error occurs (e.g., missing API key), return an empty list
        return []

    models: List[Dict[str, Any]] = []
    for model in raw_models:
        # Each model is a dict-like object; extract required fields
        model_id = model.get("id") or model.get("model_id") or ""
        model_type = model.get("type") or "model"
        created_at = model.get("created_at") or model.get("created") or None
        display_name = model.get("display_name") or model_id

        models.append(
            {
                "type": model_type,
                "id": model_id,
                "display_name": display_name,
                "created_at": created_at,
            }
        )

    return models