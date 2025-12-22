from pathlib import Path
from deep_next.core.steps.action_plan.srf.file_selection.tools.module_public_interface_lookup import (  # noqa: E501
    module_public_interface_lookup_tool_builder,
)
from deep_next.core.io import read_txt

def read_file_or_lookup_interface(root_path: Path, file_path: str) -> str:
    """Read the contents of a text file and return it as a string.

    If the file has more than {MAX_LINES} lines, return the module public interface
    lookup tool.
    """
    try:
        txt = read_txt(path=root_path / file_path)
    except FileNotFoundError:
        return f"File not found: {file_path}"

    lines = txt.split("\n")

    if len(lines) > MAX_LINES:
        return module_public_interface_lookup_tool_builder(root_path).invoke(file_path)

    # add line numbers to the text.
    txt = "\n".join([f"{str(i).rjust(4)}: {line}" for i, line in enumerate(lines, 1)])
    return txt