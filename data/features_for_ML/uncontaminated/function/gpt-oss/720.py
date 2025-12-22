import re
from pathlib import Path

def load_section(section_number):
    """
    Load the content of a section from a file named 'sections.txt'.

    The file is expected to contain sections separated by lines of the form
    '=== Section <number> ==='.  The function returns the text belonging to
    the requested section number (as an integer).  If the section is not
    found, None is returned.

    Parameters
    ----------
    section_number : int or str
        The number of the section to load.

    Returns
    -------
    str or None
        The content of the requested section, or None if not found.
    """
    # Ensure the section number is an integer
    try:
        sec_num = int(section_number)
    except Exception:
        raise ValueError("section_number must be an integer or string representing an integer")

    # Path to the sections file
    file_path = Path("sections.txt")

    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_path}' does not exist")

    # Read the entire file content
    content = file_path.read_text(encoding="utf-8")

    # Regular expression to capture sections
    # Matches lines like '=== Section 1 ===' followed by any text until the next section header or EOF
    pattern = re.compile(
        r"^=== Section\s+(\d+)\s*===\s*(.*?)\s*(?=^=== Section\s+\d+\s*===|$)",
        re.MULTILINE | re.DOTALL,
    )

    # Build a mapping from section number to its content
    sections = {}
    for match in pattern.finditer(content):
        num = int(match.group(1))
        body = match.group(2).strip()
        sections[num] = body

    # Return the requested section or None if not present
    return sections.get(sec_num)