def select_code(
    root_path: Path,
    issue_statement: str,
    git_diff: str,
) -> dict[str, list[str]]:
    """
    Select code fragments from the files in the git diff based on the issue statement.

    Use the select_related_snippets module to find the relevant code snippets based on
    the issue statement and the files present in the git diff.
    """
    from select_related_snippets import select_related_snippets
    
    # Parse the git diff to extract file paths
    files_in_diff = set()
    for line in git_diff.split('\n'):
        if line.startswith('+++') or line.startswith('---'):
            # Extract file path from diff header
            # Format: +++ b/path/to/file or --- a/path/to/file
            parts = line.split('\t')
            if len(parts) > 0:
                file_path = parts[0][6:]  # Remove '+++ b/' or '--- a/'
                if file_path and file_path != '/dev/null':
                    files_in_diff.add(file_path)
    
    # Select related snippets for each file in the diff
    result = {}
    for file_path in files_in_diff:
        full_path = root_path / file_path
        if full_path.exists() and full_path.is_file():
            try:
                snippets = select_related_snippets(
                    file_path=full_path,
                    issue_statement=issue_statement
                )
                if snippets:
                    result[file_path] = snippets
            except Exception:
                # If selection fails for a file, continue with others
                pass
    
    return result