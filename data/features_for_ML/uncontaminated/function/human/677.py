import json
from koreo.constants import (
    DEFAULT_LOAD_RETRY_DELAY,
    KOREO_DIRECTIVE_KEYS,
    LAST_APPLIED_ANNOTATION,
    PLURAL_LOOKUP_NEEDED,
)

def _extract_last_applied(resource: dict) -> dict | None:
    if not resource:
        return None

    metadata = resource.get("metadata")
    if not metadata:
        return None

    annotations = metadata.get("annotations")
    if not annotations:
        return None

    last_applied = annotations.get(LAST_APPLIED_ANNOTATION)
    if not last_applied:
        return None

    return json.loads(last_applied)