def process_json(json_data=None):
    import json
    
    if json_data is None:
        json_data = data
    
    if isinstance(json_data, str):
        try:
            parsed = json.loads(json_data)
        except json.JSONDecodeError:
            return None
    else:
        parsed = json_data
    
    if isinstance(parsed, dict):
        return {k: v for k, v in parsed.items() if v is not None}
    elif isinstance(parsed, list):
        return [item for item in parsed if item is not None]
    
    return parsed