def make_code_text(files_dict, add_line_numbers=True):
    """
    Generate a single string containing the contents of all files in `files_dict`.
    Each file is separated by a header line of the form:
        --- <filename> ---
    If `add_line_numbers` is True, each line of the file content is prefixed
    with a 4‑digit line number followed by a vertical bar and a space.
    """
    if not files_dict:
        return ""

    parts = []
    for filename in sorted(files_dict):
        parts.append(f"--- {filename} ---")
        content = files_dict[filename]
        # Ensure we work with a string
        if not isinstance(content, str):
            content = str(content)
        lines = content.splitlines(True)  # keep line endings
        for idx, line in enumerate(lines, start=1):
            if add_line_numbers:
                parts.append(f"{idx:4d} | {line.rstrip()}")
            else:
                parts.append(line.rstrip())
        # Add a blank line after each file for readability
        parts.append("")
    # Join with newlines; strip the final blank line
    return "\n".join(parts).rstrip("\n")