import httpx
from httpx import HttpUrl
from typing import Optional

class JiraIssuesClient:

    def __init__(self, issues_user: str, issues_api_key: str, httpx_client: httpx.Client) -> None:
        self.issues_user = issues_user
        self.issues_api_key = issues_api_key
        self.httpx_client = httpx_client

    def get_issue_content(self, issues_url: HttpUrl, issue_id: str) -> Optional[IssueContent]:
        response = self.httpx_client.get(issues_url + f"/{issue_id}", auth=(self.issues_user, self.issues_api_key))
        if response.status_code == 200:
            return response.json()
        else:
            return None