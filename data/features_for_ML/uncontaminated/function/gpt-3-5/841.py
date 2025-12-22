def deserialize(value: str | bytes, target_type: type[T], json: bool = False) -> T:
    import json
    
    if json:
        value = json.loads(value)
    
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    
    return target_type(value)