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
    insert_spec = change.get('insert_after_line', {})
    search_text = insert_spec.get('search_text')
    new_lines = insert_spec.get('new_lines', [])
    
    if not search_text or not new_lines:
        return
    
    # Ensure new_lines is a list
    if isinstance(new_lines, str):
        new_lines = [new_lines]
    
    # Find the line containing search_text and insert after it
    for i, line in enumerate(lines):
        if search_text in line:
            # Insert new lines after the found line
            for j, new_line in enumerate(new_lines):
                lines.insert(i + 1 + j, new_line)
            break