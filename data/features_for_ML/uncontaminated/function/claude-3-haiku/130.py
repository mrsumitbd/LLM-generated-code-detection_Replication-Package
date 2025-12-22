def get_objects(ref=None):
    if ref is None:
        return []
    else:
        try:
            return [obj for obj in ref.all()]
        except AttributeError:
            return [ref]