from pathlib import Path
import re
from typing import Dict, List

# Import the helper module that actually performs the snippet selection.
# The module is expected to expose a function named `find_related_snippets`
# which accepts an issue statement, a list of file paths, and the root path,
# and returns a mapping from file path to a list of relevant code snippets.
try:
    from select_related_snippets import find_related_snippets
except Exception:  # pragma: no cover
    # If the helper module is missing or fails to import, fall back to an empty result.
    def find_related_snippets(issue_statement: str, file_paths: List[str], root_path: Path) -> Dict[str, List[str]]:
        return {}


def _extract_file_paths_from_diff(diff_text: str) -> List[str]:
    """
    Extract the list of file paths that appear in a git diff.

    The function looks for lines that start with either:
    - `diff --git a/<path> b/<path>`
    - `+++ b/<path>`

    It returns the unique set of `<path>` values that appear after the `b/` prefix.
    """
    paths = set()
    # Pattern for the diff header line
    diff_header_re = re.compile(r"^diff --git a/(.+?) b/(.+?)$")
    # Pattern for the added file line
    added_file_re = re.compile(r"^\+\+\+ b/(.+?)$")

    for line in diff_text.splitlines():
        if m := diff_header_re.match(line):
            # Use the second path (the new file path)
            paths.add(m.group(2))
        elif m := added_file_re.match(line):
            paths.add(m.group(1))
    return sorted(paths)


def select_code(
    root_path: Path,
    issue_statement: str,
    git_diff: str,
) -> Dict[str, List[str]]:
    """
    Select code fragments from the files in the git diff based on the issue statement.

    Parameters
    ----------
    root_path : Path
        The root directory of the repository.
    issue_statement : str
        A natural‑language description of the issue that needs to be addressed.
    git_diff : str
        The raw output of a `git diff` command.

    Returns
    -------
    Dict[str, List[str]]
        A mapping from file path (relative to ``root_path``) to a list of code
        snippets that are relevant to the issue statement.
    """
    # 1. Parse the diff to get the list of affected files.
    file_paths = _extract_file_paths_from_diff(git_diff)

    # 2. Delegate the heavy lifting to the helper module.
    #    The helper is expected to read the files from ``root_path`` and
    #    return a mapping from file path to relevant snippets.
    snippets_by_file = find_related_snippets(issue_statement, file_paths, root_path)

    # 3. Ensure the return type is a plain dict with lists.
    #    The helper might return a defaultdict or other mapping; convert it.
    return {str(k): list(v) for k, v in snippets_by_file.items()}