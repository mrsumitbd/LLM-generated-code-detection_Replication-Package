def get_releases_metadata(client: GitHubGraphQLClient, owner: str, repo: str) -> GitHubReleases:
    try:
        return get_releases_metadata_cache(owner, repo)
    except KeyError:
        releases = client.get_releases(owner, repo)
        set_releases_metadata_cache(owner, repo, releases)
        return releases