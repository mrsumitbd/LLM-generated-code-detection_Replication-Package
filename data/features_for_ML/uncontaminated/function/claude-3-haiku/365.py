def process_json(json_data=data):
    import json

    try:
        data = json.loads(json_data)
        processed_data = {}

        for key, value in data.items():
            if isinstance(value, dict):
                processed_data[key] = process_json(json.dumps(value))
            else:
                processed_data[key] = value

        return processed_data
    except (ValueError, TypeError):
        return {}