def get_releases_metadata(client: GitHubGraphQLClient, owner: str, repo: str) -> GitHubReleases:
    query = """
    query($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
            releases(last: 10) {
                nodes {
                    name
                    tagName
                    description
                    publishedAt
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
    releases_data = response['data']['repository']['releases']['nodes']

    releases = []
    for release in releases_data:
        releases.append({
            'name': release['name'],
            'tag_name': release['tagName'],
            'description': release['description'],
            'published_at': release['publishedAt']
        })

    return GitHubReleases(releases)