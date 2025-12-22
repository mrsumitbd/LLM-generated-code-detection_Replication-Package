import re
import yaml

def fix_output_references(yaml_str: str) -> str:
    """Fix any broken output references in the YAML string.

    Args:
        yaml_str: The YAML string to fix

    Returns:
        The fixed YAML string
    """
    # Pattern to find ${output.<name>} references
    pattern = re.compile(r'\${output\.([A-Za-z0-9_]+)}')

    # Load YAML to extract the outputs mapping if present
    try:
        data = yaml.safe_load(yaml_str)
    except Exception:
        data = {}

    outputs = {}
    if isinstance(data, dict):
        outputs = data.get("outputs", {})
        if not isinstance(outputs, dict):
            outputs = {}

    # Replace each reference with the actual value if available
    def replace(match: re.Match) -> str:
        key = match.group(1)
        return str(outputs.get(key, match.group(0)))

    return pattern.sub(replace, yaml_str)