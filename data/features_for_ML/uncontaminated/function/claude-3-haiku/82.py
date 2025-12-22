def keep(conf):
    result = []
    for item in conf:
        if isinstance(item, dict):
            new_item = {k: v for k, v in item.items() if v is not None}
            if new_item:
                result.append(new_item)
        elif item is not None:
            result.append(item)
    return result