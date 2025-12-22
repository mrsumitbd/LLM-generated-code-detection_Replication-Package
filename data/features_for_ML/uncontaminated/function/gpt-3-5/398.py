def get_compatible_version(repo: GitHubRepo, compatibility_spec: SimpleSpec, include_dev: bool = False):
    compatible_versions = []
    for version in repo.versions:
        if compatibility_spec.match(version) and (include_dev or not version.is_dev):
            compatible_versions.append(version)
    return compatible_versions