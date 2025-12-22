def convert(path: str) -> None:
    import os
    import json
    from pathlib import Path
    
    # Get the file extension
    file_ext = os.path.splitext(path)[1].lower()
    
    # Read the file
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse based on file type
    if file_ext == '.json':
        data = json.loads(content)
        output_ext = '.yaml'
        output_content = _dict_to_yaml(data)
    elif file_ext in ['.yaml', '.yml']:
        import yaml
        data = yaml.safe_load(content)
        output_ext = '.json'
        output_content = json.dumps(data, indent=2)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    # Generate output path
    base_path = os.path.splitext(path)[0]
    output_path = base_path + output_ext
    
    # Write the converted file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)


def _dict_to_yaml(data, indent=0):
    """Convert a dictionary to YAML format string"""
    lines = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(' ' * indent + f'{key}:')
                lines.append(_dict_to_yaml(value, indent + 2))
            elif isinstance(value, list):
                lines.append(' ' * indent + f'{key}:')
                for item in value:
                    if isinstance(item, dict):
                        lines.append(' ' * (indent + 2) + '-')
                        lines.append(_dict_to_yaml(item, indent + 4))
                    else:
                        lines.append(' ' * (indent + 2) + f'- {item}')
            else:
                lines.append(' ' * indent + f'{key}: {value}')
    
    return '\n'.join(lines)