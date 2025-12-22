def _extract_last_applied(resource: dict) -> dict | None:
    return resource.get('status', {}).get('lastAppliedConfiguration') if 'status' in resource else None