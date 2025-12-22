def is_serializable(item):
    try:
        _ = json.dumps(item)
        return True
    except:
        return False