from typing import List, Dict, Any

# The following imports are assumed to exist in the surrounding codebase.
# They are imported here for type checking purposes only.
try:
    from .client import GitHubGraphQLClient
    from .models import GitHubReleases, GitHubRelease, GitHubReleaseAsset
except Exception:
    # If the imports fail (e.g., during static analysis), we define minimal stubs
    # so that the function can still be type‑checked. These stubs will be
    # replaced by the real implementations in the actual project.
    class GitHubGraphQLClient:
        def execute(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
            raise NotImplementedError

    class GitHubReleaseAsset:
        def __init__(self, name: str, download_url: str, size: int):
            self.name = name
            self.download_url = download_url
            self.size = size

    class GitHubRelease:
        def __init__(
            self,
            tag_name: str,
            name: str,
            published_at: str,
            prerelease: bool,
            draft: bool,
            url: str,
            assets: List[GitHubReleaseAsset],
        ):
            self.tag_name = tag_name
            self.name = name
            self.published_at = published_at
            self.prerelease = prerelease
            self.draft = draft
            self.url = url
            self.assets = assets

    class GitHubReleases:
        def __init__(self, releases: List[GitHubRelease]):
            self.releases = releases


def _build_release_from_node(node: Dict[str, Any]) -> GitHubRelease:
    """Convert a GraphQL release node into a GitHubRelease instance."""
    assets = [
        GitHubReleaseAsset(
            name=asset["name"],
            download_url=asset["downloadUrl"],
            size=asset["size"],
        )
        for asset in node.get("assets", {}).get("nodes", [])
    ]

    return GitHubRelease(
        tag_name=node.get("tagName", ""),
        name=node.get("name", ""),
        published_at=node.get("publishedAt", ""),
        prerelease=node.get("prerelease", False),
        draft=node.get("draft", False),
        url=node.get("url", ""),
        assets=assets,
    )


def get_releases_metadata(
    client: GitHubGraphQLClient, owner: str, repo: str
) -> GitHubReleases:
    """
    Retrieve all releases for the specified repository using the GitHub GraphQL API.

    Parameters
    ----------
    client : GitHubGraphQLClient
        A client capable of executing GraphQL queries against GitHub.
    owner : str
        Repository owner (user or organization).
    repo : str
        Repository name.

    Returns
    -------
    GitHubReleases
        An object containing a list of all releases for the repository.
    """
    # GraphQL query to fetch releases with pagination
    query = """
    query ($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        releases(first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            tagName
            name
            publishedAt
            prerelease
            draft
            url
            assets(first: 100) {
              nodes {
                name
                downloadUrl
                size
              }
            }
          }
        }
      }
    }
    """

    releases: List[GitHubRelease] = []
    cursor: str | None = None

    while True:
        variables = {"owner": owner, "name": repo, "cursor": cursor}
        result = client.execute(query, variables)

        # Navigate the nested structure safely
        repo_data = result.get("data", {}).get("repository")
        if not repo_data:
            break

        releases_data = repo_data.get("releases", {})
        nodes = releases_data.get("nodes", [])
        for node in nodes:
            releases.append(_build_release_from_node(node))

        page_info = releases_data.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return GitHubReleases(releases=releases)