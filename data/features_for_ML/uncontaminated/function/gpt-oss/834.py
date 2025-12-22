import os
from typing import List, Any

def apply_prompt_template(prompt_name: str, state: Any, template: str = None) -> List[str]:
    """
    Load a prompt template (either from the provided `template` string or from a file named
    `<prompt_name>.txt` in the current working directory), format it with the attributes
    of `state`, and return the resulting prompt split into a list of lines.

    Parameters
    ----------
    prompt_name : str
        The base name of the template file to load if `template` is None.
    state : Any
        An object or mapping whose keys/attributes will be used for formatting.
    template : str, optional
        A template string containing Python format placeholders. If None, the function
        will attempt to read a file named `<prompt_name>.txt` from the current working
        directory.

    Returns
    -------
    List[str]
        The formatted prompt split into individual lines.

    Raises
    ------
    FileNotFoundError
        If `template` is None and the corresponding file cannot be found.
    KeyError
        If a placeholder in the template cannot be resolved from `state`.
    """
    # Determine the template string
    if template is None:
        # Try to load from a file named "<prompt_name>.txt" in the current directory
        file_path = os.path.join(os.getcwd(), f"{prompt_name}.txt")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Template file '{file_path}' not found.")
        with open(file_path, "r", encoding="utf-8") as f:
            template_str = f.read()
    else:
        template_str = template

    # Prepare the context for formatting
    if isinstance(state, dict):
        context = state
    else:
        # Use the object's __dict__ if available, otherwise try vars()
        try:
            context = state.__dict__
        except AttributeError:
            context = vars(state)

    # Format the template
    try:
        formatted = template_str.format(**context)
    except KeyError as e:
        raise KeyError(f"Missing key for template formatting: {e}") from e

    # Split into lines and return
    return formatted.splitlines()