import json

def get_fixed_tool_calls_or_text_output(json_str, max_depth=5):
    def traverse_json(data, current_depth):
        if current_depth > max_depth:
            return []

        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if key == "tool_call":
                    result.append(value)
                else:
                    result.extend(traverse_json(value, current_depth + 1))
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                result.extend(traverse_json(item, current_depth + 1))
            return result
        else:
            return []

    data = json.loads(json_str)
    return traverse_json(data, 1)