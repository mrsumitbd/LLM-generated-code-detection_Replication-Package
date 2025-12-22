def get_fixed_tool_calls_or_text_output(json_str, max_depth=5):
    import json

    def get_tool_calls_or_text(data, depth):
        if depth == 0:
            return []
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if key == 'tool_calls' and isinstance(value, list):
                    result.extend(value)
                else:
                    result.extend(get_tool_calls_or_text(value, depth - 1))
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                result.extend(get_tool_calls_or_text(item, depth))
            return result
        else:
            return []

    try:
        data = json.loads(json_str)
        return get_tool_calls_or_text(data, max_depth)
    except json.JSONDecodeError:
        return []