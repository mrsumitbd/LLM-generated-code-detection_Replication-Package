def is_repo_id_cached(repo_id: int) -> bool:
    """Check if a repository ID exists in the local cache.

    Args:
        repo_id: The repository ID to check

    Returns:
        True if the repository ID is found in cache, False otherwise.
    """
    try:
        with open('cache.json', 'r') as f:
            cache = json.load(f)
        return repo_id in cache
    except (FileNotFoundError, json.JSONDecodeError):
        return False