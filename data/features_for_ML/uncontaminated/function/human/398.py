import logging
from semantic_version import SimpleSpec, Version

def get_compatible_version(repo: GitHubRepo, compatibility_spec: SimpleSpec, include_dev: bool = False):
    all_versions = get_available_versions(repo)

    # Filter out dev versions if include_dev is False
    if not include_dev:
        filtered_versions = []
        for version in all_versions:
            tag_name = getattr(version, "_origin_tag_name", str(version))
            if not is_dev_version(tag_name):
                filtered_versions.append(version)
        all_versions = filtered_versions

    versions = sorted(compatibility_spec.filter(all_versions))[-10:]
    if not versions:
        return
    logging.info(f"Available versions: {tuple(map(str, versions))}")
    return versions[-1]