import re
import click

def validate_pattern_for_direct_mode(ctx, param, value):
    """
    Validate a pattern string used in direct mode.

    The pattern is expected to be a valid regular expression.  It must not be
    empty and must compile without errors.  If the pattern is invalid a
    click.BadParameter exception is raised.

    Parameters
    ----------
    ctx : click.Context
        The click context (unused).
    param : click.Parameter
        The click parameter (unused).
    value : str
        The pattern string to validate.

    Returns
    -------
    str
        The original pattern string if it is valid.

    Raises
    ------
    click.BadParameter
        If the pattern is empty or cannot be compiled as a regular
        expression.
    """
    # Ensure the value is a string
    if not isinstance(value, str):
        raise click.BadParameter("Pattern must be a string")

    # Empty pattern is not allowed
    if not value:
        raise click.BadParameter("Pattern cannot be empty")

    # Try to compile the pattern to ensure it is a valid regex
    try:
        re.compile(value)
    except re.error as exc:
        raise click.BadParameter(f"Invalid regular expression: {exc}") from exc

    return value