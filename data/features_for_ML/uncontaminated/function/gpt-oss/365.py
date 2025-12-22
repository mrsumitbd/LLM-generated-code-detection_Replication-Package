import json

# Default JSON data (empty object)
data = "{}"

def process_json(json_data=data):
    """
    Parse the given JSON data and return the corresponding Python object.
    If the input is already a dict or list, it is returned unchanged.
    Raises ValueError if the JSON string is invalid.
    Raises TypeError for unsupported input types.
    """
    if isinstance(json_data, str):
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc
    elif isinstance(json_data, (dict, list)):
        return json_data
    else:
        raise TypeError("json_data must be a JSON string, dict, or list")