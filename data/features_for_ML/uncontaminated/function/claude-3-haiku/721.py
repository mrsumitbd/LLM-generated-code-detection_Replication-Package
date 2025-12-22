from typing import List
from dataclasses import dataclass

@dataclass
class GitHubRelease:
    tag_name: str
    name: str
    published_at: str
    html_url: str

GitHubReleases = List[GitHubRelease]

def get_releases_metadata(client: GitHubGraphQLClient, owner: str, repo: str) -> GitHubReleases:
    query = """
    query($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
            releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    tagName
                    name
                    publishedAt
                    url
                }
            }
        }
    }
    """

    variables = {
        "owner": owner,
        "repo": repo
    }

    response = client.execute(query, variables)
    releases = response["data"]["repository"]["releases"]["nodes"]

    return [
        GitHubRelease(
            tag_name=release["tagName"],
            name=release["name"],
            published_at=release["publishedAt"],
            html_url=release["url"]
        )
        for release in releases
    ]