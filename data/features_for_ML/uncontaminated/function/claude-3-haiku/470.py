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
    insert_after = change['insert_after_line']
    content_to_insert = change['content']

    for i, line in enumerate(lines):
        if insert_after in line:
            lines.insert(i + 1, content_to_insert)
            break