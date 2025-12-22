import json
from typing import Any, Dict, Optional

def _extract_last_applied(resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extract the last applied configuration from a Kubernetes resource.

    The last applied configuration is stored in the annotation
    `kubectl.kubernetes.io/last-applied-configuration`. This function
    retrieves that annotation, parses it as JSON, and returns the resulting
    dictionary. If the annotation is missing or cannot be parsed, `None`
    is returned.

    Parameters
    ----------
    resource : dict
        The Kubernetes resource object.

    Returns
    -------
    dict | None
        The parsed last applied configuration, or None if not available.
    """
    annotations = resource.get("metadata", {}).get("annotations", {})
    last_applied = annotations.get("kubectl.kubernetes.io/last-applied-configuration")
    if not last_applied:
        return None
    try:
        return json.loads(last_applied)
    except (json.JSONDecodeError, TypeError):
        return None