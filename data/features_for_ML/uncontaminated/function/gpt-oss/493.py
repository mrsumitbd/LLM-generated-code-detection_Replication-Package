from typing import Optional
import urllib.parse

def make_vcs_requirement_url(
    repo_url: str, rev: str, project_name: str, subdir: Optional[str] = None
) -> str:
    """
    Return the URL for a VCS requirement.

    Args:
      repo_url: the remote VCS url, with any needed VCS prefix (e.g. "git+").
      project_name: the (unescaped) project name.
      rev: the revision (branch, tag, commit) to pin to.
      subdir: optional subdirectory within the repository.

    Returns:
        A string suitable for use as a VCS requirement in a pip install
        command, e.g. "git+https://github.com/user/repo.git@v1.2#egg=proj".
    """
    # Build the base requirement string
    if rev:
        base = f"{repo_url}@{rev}"
    else:
        base = repo_url

    # Encode the egg name (project name) to be safe in URLs
    egg = urllib.parse.quote(project_name, safe="")

    # Build the fragment part
    fragment = f"egg={egg}"
    if subdir:
        # Ensure subdir is URL‑encoded
        subdir_enc = urllib.parse.quote(subdir, safe="/")
        fragment += f"&subdirectory={subdir_enc}"

    return f"{base}#{fragment}"