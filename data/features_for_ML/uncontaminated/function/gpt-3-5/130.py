def get_objects(ref=None):
    if ref is None:
        return []
    else:
        return [obj for obj in ref if isinstance(obj, object)]