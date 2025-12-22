def _extract_last_applied(resource: dict) -> dict | None:
    if 'metadata' not in resource or 'annotations' not in resource['metadata']:
        return None

    annotations = resource['metadata']['annotations']
    if 'kubectl.kubernetes.io/last-applied-configuration' not in annotations:
        return None

    try:
        return json.loads(annotations['kubectl.kubernetes.io/last-applied-configuration'])
    except (ValueError, KeyError):
        return None