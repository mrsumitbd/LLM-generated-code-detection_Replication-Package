def _parse_from_test_patch(test_patch: str, func_name: str) -> str:
    """
    Extract the added function definition for `func_name` from a unified diff patch.

    Parameters
    ----------
    test_patch : str
        The full diff patch as a string.
    func_name : str
        The name of the function to extract.

    Returns
    -------
    str
        The function definition (including the `def` line and its body) as a string
        without the diff prefixes. If the function is not found, an empty string
        is returned.
    """
    lines = test_patch.splitlines()
    captured = []
    def_found = False
    def_indent = None

    for i, raw_line in enumerate(lines):
        # Only consider added lines
        if not raw_line.startswith('+'):
            continue

        line = raw_line[1:]  # strip the '+' prefix

        # Skip context lines that are not part of the added block
        if not def_found:
            # Look for the function definition line
            if line.lstrip().startswith(f'def {func_name}('):
                def_found = True
                # Determine indentation of the def line
                def_indent = len(line) - len(line.lstrip())
                captured.append(line)
            continue

        # After the def line has been found, capture body lines
        # Stop if we hit a line that is not part of the function body
        # (i.e., not indented more than the def line or not an added line)
        if not raw_line.startswith('+'):
            break

        # Strip the '+' prefix again
        body_line = raw_line[1:]

        # If the line is a decorator or blank, include it
        if body_line.lstrip().startswith('@') or body_line.strip() == '':
            captured.append(body_line)
            continue

        # Determine indentation of the current line
        curr_indent = len(body_line) - len(body_line.lstrip())

        # If indentation is less than or equal to def_indent, we are out of the function
        if curr_indent <= def_indent:
            break

        captured.append(body_line)

    return '\n'.join(captured)