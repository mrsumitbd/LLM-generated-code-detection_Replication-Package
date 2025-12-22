from pathlib import Path
from select_related_snippets import select_related_snippets

def select_code(
    root_path: Path,
    issue_statement: str,
    git_diff: str,
) -> dict[str, list[str]]:
    code_snippets = select_related_snippets(root_path, issue_statement, git_diff)
    return code_snippets