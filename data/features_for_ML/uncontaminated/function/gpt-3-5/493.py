def make_vcs_requirement_url(repo_url: str, rev: str, project_name: str, subdir: Optional[str] = None) -> str:
    if subdir:
        return f"{repo_url}#egg={project_name}&subdirectory={subdir}&rev={rev}"
    else:
        return f"{repo_url}#egg={project_name}&rev={rev}"