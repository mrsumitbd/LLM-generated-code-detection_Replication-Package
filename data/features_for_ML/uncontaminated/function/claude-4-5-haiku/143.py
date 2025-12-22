def is_repo_id_cached(repo_id: int) -> bool:
    """Check if a repository ID exists in the local cache.

    Args:
        repo_id: The repository ID to check

    Returns:
        True if the repository ID is found in cache, False otherwise.
    """
    import os
    from pathlib import Path
    
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    if not cache_dir.exists():
        return False
    
    for item in cache_dir.iterdir():
        if item.is_dir() and item.name.startswith("models--"):
            repo_id_str = item.name.replace("models--", "").replace("--", "/")
            if repo_id_str == str(repo_id):
                return True
    
    return False