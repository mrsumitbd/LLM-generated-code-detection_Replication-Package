import json
import os
from typing import Set

# Global cache set to avoid repeated file reads
_repo_cache_set: Set[int] | None = None
_cache_file_path = os.path.join(os.path.dirname(__file__), "repo_cache.json")


def _load_cache() -> Set[int]:
    """Load the repository ID cache from disk into a set."""
    global _repo_cache_set
    if _repo_cache_set is not None:
        return _repo_cache_set

    if not os.path.exists(_cache_file_path):
        _repo_cache_set = set()
        return _repo_cache_set

    try:
        with open(_cache_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Expecting a list of integers
            if isinstance(data, list):
                _repo_cache_set = {int(x) for x in data if isinstance(x, int)}
            else:
                _repo_cache_set = set()
    except Exception:
        # If any error occurs, treat cache as empty
        _repo_cache_set = set()

    return _repo_cache_set


def is_repo_id_cached(repo_id: int) -> bool:
    """Check if a repository ID exists in the local cache.

    Args:
        repo_id: The repository ID to check

    Returns:
        True if the repository ID is found in cache, False otherwise.
    """
    cache_set = _load_cache()
    return repo_id in cache_set