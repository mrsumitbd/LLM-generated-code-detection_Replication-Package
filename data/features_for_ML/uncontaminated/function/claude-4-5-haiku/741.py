import json

def is_serializable(item):
    try:
        json.dumps(item)
        return True
    except (TypeError, ValueError):
        return False