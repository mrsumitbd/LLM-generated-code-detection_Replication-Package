from __future__ import annotations

from typing import Optional

from github import Github, Repository, Organization, GithubException

# Assume Consts is defined elsewhere in the package
try:
    from .consts import Consts
except Exception:  # pragma: no cover
    class Consts:  # minimal fallback
        DEFAULT_BASE_URL = "https://api.github.com"


class GithubClient:
    """Manages interaction with GitHub"""

    def __init__(self, token: str | None = None, base_url: str = Consts.DEFAULT_BASE_URL):
        self._token = token
        self._base_url = base_url
        self._client: Optional[Github] = None

    @property
    def client(self) -> Github:
        if self._client is None:
            self._client = Github(login_or_token=self._token, base_url=self._base_url)
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