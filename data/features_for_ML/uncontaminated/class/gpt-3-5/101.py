from github import Github
from github.Repository import Repository
from github.Organization import Organization

class GithubClient:
    """Manages interaction with GitHub"""

    def __init__(self, token: str | None = None, base_url: str = Consts.DEFAULT_BASE_URL):
        self.token = token
        self.base_url = base_url

    @property
    def client(self) -> Github:
        if self.token:
            return Github(self.token, base_url=self.base_url)
        else:
            return Github(base_url=self.base_url)

    def get_repo_by_full_name(self, full_name: str) -> Repository | None:
        try:
            return self.client.get_repo(full_name)
        except Exception:
            return None

    def get_organization(self, org_name: str) -> Organization | None:
        try:
            return self.client.get_organization(org_name)
        except Exception:
            return None