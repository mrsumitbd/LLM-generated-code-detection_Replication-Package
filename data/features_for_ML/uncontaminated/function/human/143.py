def is_repo_id_cached(repo_id: int) -> bool:
    """Check if a repository ID exists in the local cache.

    Args:
        repo_id: The repository ID to check

    Returns:
        True if the repository ID is found in cache, False otherwise.
    """
    cached_repos = get_cached_repositories()
    if not cached_repos:
        return False

    return any(repo.get("id") == repo_id for repo in cached_repos)