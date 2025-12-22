from packaging.version import Version, InvalidVersion
from typing import Optional, Iterable

def get_compatible_version(repo: "GitHubRepo",
                           compatibility_spec: "SimpleSpec",
                           include_dev: bool = False) -> Optional[str]:
    """
    Return the highest tag from *repo* that satisfies *compatibility_spec*.
    If *include_dev* is False, pre‑release tags (e.g. 1.0.0a1, 1.0.0b2, 1.0.0rc1) are ignored.
    If no tag matches, ``None`` is returned.
    """
    # Retrieve all tag names from the repository
    try:
        tags: Iterable[str] = repo.get_tags()
    except AttributeError:
        # Fallback: try a generic attribute
        tags = getattr(repo, "tags", [])

    # Convert tag names to Version objects, filtering out invalid ones
    versions = []
    for tag in tags:
        try:
            v = Version(tag)
        except InvalidVersion:
            continue
        # Skip pre‑releases unless include_dev is True
        if not include_dev and v.is_prerelease:
            continue
        versions.append(v)

    # If no versions are available, return None
    if not versions:
        return None

    # Filter versions that satisfy the compatibility spec
    compatible = [v for v in versions if compatibility_spec.match(v)]

    if not compatible:
        return None

    # Return the highest compatible version as a string
    return str(max(compatible))