def make_vcs_requirement_url(
    repo_url: str, rev: str, project_name: str, subdir: Optional[str] = None
) -> str:
    """
    Return the URL for a VCS requirement.

    Args:
      repo_url: the remote VCS url, with any needed VCS prefix (e.g. "git+").
      project_name: the (unescaped) project name.
    """
    if subdir:
        repo_url = f"{repo_url}#subdirectory={subdir}"
    return f"{repo_url}@{rev}#egg={project_name}"