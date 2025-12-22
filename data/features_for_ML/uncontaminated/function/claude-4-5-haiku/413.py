def fix_output_references(yaml_str: str) -> str:
    """Fix any broken output references in the YAML string.

    Args:
        yaml_str: The YAML string to fix

    Returns:
        The fixed YAML string
    """
    import re
    
    # Pattern to match broken output references like ${{ outputs.step_id.output_name }}
    # where step_id or output_name might be missing or malformed
    
    # Fix references that are missing the 'steps.' prefix
    # Pattern: ${{ outputs.something }} -> ${{ steps.something.outputs.* }}
    yaml_str = re.sub(
        r'\$\{\{\s*outputs\.([a-zA-Z0-9_-]+)\.([a-zA-Z0-9_-]+)\s*\}\}',
        r'${{ steps.\1.outputs.\2 }}',
        yaml_str
    )
    
    # Fix references with just outputs.step_id (missing output name)
    # This pattern catches ${{ outputs.step_id }} and converts to proper format
    yaml_str = re.sub(
        r'\$\{\{\s*outputs\.([a-zA-Z0-9_-]+)\s*\}\}',
        r'${{ steps.\1.outputs.result }}',
        yaml_str
    )
    
    # Fix malformed references like ${{ output.* }} (missing 's')
    yaml_str = re.sub(
        r'\$\{\{\s*output\.([a-zA-Z0-9_-]+)\.([a-zA-Z0-9_-]+)\s*\}\}',
        r'${{ steps.\1.outputs.\2 }}',
        yaml_str
    )
    
    # Fix references with extra spaces
    yaml_str = re.sub(
        r'\$\{\{\s+steps\.([a-zA-Z0-9_-]+)\.outputs\.([a-zA-Z0-9_-]+)\s+\}\}',
        r'${{ steps.\1.outputs.\2 }}',
        yaml_str
    )
    
    return yaml_str