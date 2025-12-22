class GithubClient:
    """Manages interaction with GitHub"""

    def __init__(self, token: str | None = None, base_url: str = Consts.DEFAULT_BASE_URL):
        self._token = token
        self._base_url = base_url
        self._client = None

    @property
    def client(self) -> Github:
        if self._client is None:
            if self._token:
                self._client = Github(auth=Auth.Token(self._token), base_url=self._base_url)
            else:
                self._client = Github(base_url=self._base_url)
        return self._client

    def get_repo_by_full_name(self, full_name: str) -> Repository | None:
        try:
            return self.client.get_repo(full_name)
        except GithubException:
            return None

    def get_organization(self, org_name: str) -> Organization | None:
        try:
            return self.client.get_organization(org_name)
        except GithubException:
            return None