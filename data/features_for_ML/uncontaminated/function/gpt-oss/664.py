from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Union

__all__ = ["list_providers"]


def _load_json_file(path: Path) -> Union[List[Any], Dict[str, Any], None]:
    """
    Load a JSON file if it exists and is readable.

    Returns:
        The parsed JSON object or None if the file does not exist or cannot be parsed.
    """
    if not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _normalize_provider_entry(entry: Any, default_name: str | None) -> Dict[str, Any]:
    """
    Convert a provider entry into a dictionary with 'name' and 'is_default' keys.
    """
    if isinstance(entry, str):
        name = entry
    elif isinstance(entry, dict) and "name" in entry:
        name = entry["name"]
    else:
        # Unsupported format; skip this entry
        return None

    is_default = default_name is not None and name == default_name
    return {"name": name, "is_default": is_default}


def list_providers() -> List[Dict[str, Any]]:
    """
    List all configured providers.

    The function looks for provider configuration in the following order:

    1. A JSON file named ``providers.json`` located in the same directory as this module.
    2. Environment variables ``TELERT_PROVIDERS`` (comma‑separated names) and
       ``TELERT_DEFAULT_PROVIDER`` (single name).
    3. If neither source is available, an empty list is returned.

    The JSON file may contain either:

    * A list of provider names or dictionaries with a ``name`` key.
    * A dictionary with a ``providers`` key containing the list above.
    * A dictionary with a ``default`` key specifying the default provider name.

    Example JSON:

    .. code-block:: json

        {
            "providers": [
                "aws",
                {"name": "gcp"},
                "azure"
            ],
            "default": "aws"
        }

    Returns:
        A list of dictionaries with provider information.
    """
    providers: List[Dict[str, Any]] = []

    # 1. Try to load from a JSON file in the same directory
    module_dir = Path(__file__).parent
    json_path = module_dir / "providers.json"
    data = _load_json_file(json_path)

    if data is not None:
        # Extract provider list
        if isinstance(data, dict):
            provider_list = data.get("providers", [])
            default_name = data.get("default")
        else:
            provider_list = data
            default_name = None

        for entry in provider_list:
            provider = _normalize_provider_entry(entry, default_name)
            if provider:
                providers.append(provider)

        # If the JSON file did not specify a default, mark the first provider as default
        if providers and not any(p["is_default"] for p in providers):
            providers[0]["is_default"] = True

        return providers

    # 2. Try environment variables
    env_providers = os.getenv("TELERT_PROVIDERS")
    env_default = os.getenv("TELERT_DEFAULT_PROVIDER")

    if env_providers:
        names = [name.strip() for name in env_providers.split(",") if name.strip()]
        for name in names:
            providers.append({"name": name, "is_default": False})

        # Mark default if specified
        if env_default:
            for p in providers:
                if p["name"] == env_default:
                    p["is_default"] = True
                    break
        else:
            # If no default specified, mark the first provider as default
            if providers:
                providers[0]["is_default"] = True

        return providers

    # 3. No configuration found
    return providers