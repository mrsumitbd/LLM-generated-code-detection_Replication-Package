import re
import yaml

def fix_output_references(yaml_str: str) -> str:
    """Fix any broken output references in the YAML string.

    Args:
        yaml_str: The YAML string to fix

    Returns:
        The fixed YAML string
    """
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError:
        return yaml_str

    def fix_references(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    obj[key] = re.sub(r'\${(\w+)}', r'${\1}', value)
                else:
                    obj[key] = fix_references(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                obj[i] = fix_references(item)
        return obj

    fixed_data = fix_references(data)
    return yaml.dump(fixed_data)