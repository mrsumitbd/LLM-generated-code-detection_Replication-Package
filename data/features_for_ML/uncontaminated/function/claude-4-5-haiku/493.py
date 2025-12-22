def make_vcs_requirement_url(
    repo_url: str, rev: str, project_name: str, subdir: Optional[str] = None
) -> str:
    """
    Return the URL for a VCS requirement.

    Args:
      repo_url: the remote VCS url, with any needed VCS prefix (e.g. "git+").
      project_name: the (unescaped) project name.
    """
    from urllib.parse import quote
    
    # Escape the project name for use in URL
    escaped_project_name = quote(project_name, safe="")
    
    # Build the URL with the repo_url, revision, and project name
    url = f"{repo_url}@{rev}#egg={escaped_project_name}"
    
    # Add subdirectory if provided
    if subdir:
        url += f"&subdirectory={quote(subdir, safe='')}"
    
    return url