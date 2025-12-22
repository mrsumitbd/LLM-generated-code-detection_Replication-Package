from typing import Optional, Dict, Any

def build_query_params(options: Optional["QueryOptions"] = None) -> Dict[str, str]:
    """
    Build OData query parameters dict from options

    Args:
        options: Query options to convert

    Returns:
        Dictionary of query parameters
    """
    if options is None:
        return {}

    params: Dict[str, str] = {}
    # Use the public attributes of the options object
    for attr, value in vars(options).items():
        if value is None:
            continue

        # Skip empty lists or empty strings
        if isinstance(value, (list, tuple)) and not value:
            continue
        if isinstance(value, str) and not value.strip():
            continue

        # Build the key with $ prefix
        key = f"${attr}"

        # Handle list/tuple values (comma separated)
        if isinstance(value, (list, tuple)):
            params[key] = ",".join(str(v) for v in value)
            continue

        # Handle boolean values (only include if True)
        if isinstance(value, bool):
            if value:
                params[key] = "true"
            continue

        # For all other types, convert to string
        params[key] = str(value)

    return params