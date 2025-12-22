from typing import FrozenSet

def format_name(project: str, extras: FrozenSet[str]) -> str:
    """
    Format a project name with optional extras.

    Parameters
    ----------
    project : str
        The normalized project name.
    extras : FrozenSet[str]
        A set of normalized extra names.

    Returns
    -------
    str
        The formatted name, e.g. "project[extra1,extra2]" or just "project" if no extras.
    """
    if not extras:
        return project
    # Sort extras for deterministic output
    sorted_extras = sorted(extras)
    return f"{project}[{','.join(sorted_extras)}]"