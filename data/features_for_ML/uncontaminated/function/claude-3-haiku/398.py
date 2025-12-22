from packaging.version import Version
from packaging.specifiers import SpecifierSet

def get_compatible_version(repo: GitHubRepo, compatibility_spec: SimpleSpec, include_dev: bool = False):
    """
    Finds the latest version of the repository that satisfies the given compatibility specification.

    Args:
        repo (GitHubRepo): The GitHub repository object.
        compatibility_spec (SimpleSpec): The compatibility specification to match against.
        include_dev (bool, optional): Whether to include development versions. Defaults to False.

    Returns:
        Version: The latest compatible version, or None if no compatible version is found.
    """
    versions = [Version(tag.name) for tag in repo.get_tags()]
    if not include_dev:
        versions = [v for v in versions if not v.is_prerelease]

    compatible_versions = [v for v in versions if v in compatibility_spec]
    if compatible_versions:
        return max(compatible_versions)
    else:
        return None