def is_serializable(item):
    try:
        import json
        json.dumps(item)
        return True
    except (TypeError, OverflowError):
        return False