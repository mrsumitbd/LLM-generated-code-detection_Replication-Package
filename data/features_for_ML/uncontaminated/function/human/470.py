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
    insert_after_text = change["insert_after_line"]
    logger.info(f"insert_after_line '{insert_after_text}'")

    # Get the new content
    new_content = change["new_content"]

    # Find the line to insert after
    found = False
    for i, line in enumerate(lines):
        if insert_after_text.strip() in line.strip():
            # Prepare the new content
            new_lines = [
                line + ("\n" if not line.endswith("\n") else "")
                for line in new_content.split("\n")
            ]
            # Insert after the matching line
            lines = lines[:i + 1] + new_lines + lines[i + 1:]

            message = f"Inserting content after line containing '{insert_after_text}' in {filepath}"
            logger.info(message)

            found = True
            break

    if not found:
        message = f"Warning: Could not find line '{insert_after_text}' in {filepath}"
        logger.warning(message)