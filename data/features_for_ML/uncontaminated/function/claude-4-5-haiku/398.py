def get_compatible_version(repo: GitHubRepo, compatibility_spec: SimpleSpec, include_dev: bool = False):
    """
    Get a compatible version from a GitHub repository that matches the given specification.
    
    Args:
        repo: GitHubRepo object containing repository information
        compatibility_spec: SimpleSpec object with version constraints
        include_dev: Whether to include development versions
    
    Returns:
        A compatible version string, or None if no compatible version is found
    """
    from packaging.version import Version
    
    if not hasattr(repo, 'releases') or not repo.releases:
        return None
    
    compatible_versions = []
    
    for release in repo.releases:
        version_str = release.tag_name.lstrip('v')
        
        try:
            version = Version(version_str)
        except:
            continue
        
        if not include_dev and version.is_devrelease:
            continue
        
        if version in compatibility_spec:
            compatible_versions.append(version)
    
    if not compatible_versions:
        return None
    
    compatible_versions.sort(reverse=True)
    return str(compatible_versions[0])