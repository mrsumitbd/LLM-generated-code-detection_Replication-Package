def _format_json_to_markdown(json_str):
    import json

    def format_json(data, indent=0):
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                lines.append(' ' * indent + f'- **{key}**: {format_json(value, indent + 2)}')
            return '\n'.join(lines)
        elif isinstance(data, list):
            lines = []
            for item in data:
                lines.append(' ' * indent + f'- {format_json(item, indent + 2)}')
            return '\n'.join(lines)
        else:
            return json.dumps(data)

    try:
        json_data = json.loads(json_str)
        return format_json(json_data)
    except json.JSONDecodeError:
        return "Invalid JSON string provided."