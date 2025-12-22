import click
import re

def validate_pattern_for_direct_mode(ctx, param, value):
    """Validate that the pattern is a valid regex when in direct mode."""
    if value is None:
        return value
    
    # Check if we're in direct mode
    direct_mode = ctx.params.get('direct', False)
    
    if direct_mode:
        # Validate that the pattern is a valid regex
        try:
            re.compile(value)
        except re.error as e:
            raise click.BadParameter(f"Invalid regex pattern: {e}")
    
    return value