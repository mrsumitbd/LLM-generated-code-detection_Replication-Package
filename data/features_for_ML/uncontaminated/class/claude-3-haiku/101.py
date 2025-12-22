from github import Github

from .consts import Consts

class GithubClient:
    """Manages interaction with GitHub"""

    def __init__(self, token: str | None = None, base_url: str = Consts.DEFAULT_BASE_URL):
        self._token = token
        self._base_url = base_url
        self._client = Github(self._token, base_url=self._base_url)

    @property
    def client(self) -> Github:
        return self._client

    def get_repo_by_full_name(self, full_name: str) -> Repository | None:
        try:
            return self._client.get_repo(full_name)
        except:
            return None

    def get_organization(self, org_name: str) -> Organization | None:
        try:
            return self._client.get_organization(org_name)
        except:
            return None