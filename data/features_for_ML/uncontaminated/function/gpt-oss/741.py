import json

def is_serializable(item):
    """
    Return True if the given item can be serialized to JSON, False otherwise.
    """
    try:
        json.dumps(item)
        return True
    except (TypeError, OverflowError):
        return False