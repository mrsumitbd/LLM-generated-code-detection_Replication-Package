def insert_after_line(change, lines, filepath):
    """
    Insert content after a line containing specific text.

    Args:
        change: The change specification containing insert_after_line
        lines: List of file lines to modify
        filepath: Path to the file being modified

    Returns:
        None - modifies lines in place
    """
    # Determine the marker text and the content to insert
    marker = change.get("after") or change.get("line")
    content = change.get("content")

    if marker is None or content is None:
        raise ValueError(
            f"Change specification for {filepath} must contain 'after' (or 'line') and 'content' keys."
        )

    # Find the first line that contains the marker text
    target_index = None
    for idx, line in enumerate(lines):
        if marker in line:
            target_index = idx
            break

    if target_index is None:
        raise ValueError(
            f"Could not find a line containing '{marker}' in {filepath}."
        )

    # Prepare the new lines to insert
    # Preserve line endings; if the last line of content lacks a newline, add one
    new_lines = content.splitlines(True)  # keepends=True
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"

    # Insert the new lines after the target line
    lines[target_index + 1 : target_index + 1] = new_lines