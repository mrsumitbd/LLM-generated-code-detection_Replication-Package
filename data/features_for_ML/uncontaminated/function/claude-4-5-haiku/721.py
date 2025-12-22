def get_releases_metadata(client: GitHubGraphQLClient, owner: str, repo: str) -> GitHubReleases:
    query = """
    query($owner: String!, $repo: String!, $first: Int!) {
        repository(owner: $owner, name: $repo) {
            releases(first: $first, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    id
                    name
                    tagName
                    description
                    isDraft
                    isPrerelease
                    createdAt
                    publishedAt
                    url
                    author {
                        login
                        url
                    }
                    assets(first: 10) {
                        nodes {
                            id
                            name
                            downloadUrl
                            size
                            createdAt
                            updatedAt
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
    """
    
    variables = {
        "owner": owner,
        "repo": repo,
        "first": 100
    }
    
    response = client.execute(query, variables)
    
    releases_data = response.get("data", {}).get("repository", {}).get("releases", {})
    nodes = releases_data.get("nodes", [])
    page_info = releases_data.get("pageInfo", {})
    
    releases = []
    for node in nodes:
        release = GitHubRelease(
            id=node.get("id"),
            name=node.get("name"),
            tag_name=node.get("tagName"),
            description=node.get("description"),
            is_draft=node.get("isDraft", False),
            is_prerelease=node.get("isPrerelease", False),
            created_at=node.get("createdAt"),
            published_at=node.get("publishedAt"),
            url=node.get("url"),
            author=GitHubUser(
                login=node.get("author", {}).get("login"),
                url=node.get("author", {}).get("url")
            ) if node.get("author") else None,
            assets=[
                GitHubAsset(
                    id=asset.get("id"),
                    name=asset.get("name"),
                    download_url=asset.get("downloadUrl"),
                    size=asset.get("size"),
                    created_at=asset.get("createdAt"),
                    updated_at=asset.get("updatedAt")
                )
                for asset in node.get("assets", {}).get("nodes", [])
            ]
        )
        releases.append(release)
    
    return GitHubReleases(
        releases=releases,
        page_info=GitHubPageInfo(
            has_next_page=page_info.get("hasNextPage", False),
            end_cursor=page_info.get("endCursor")
        )
    )