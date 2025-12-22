import httpx
from typing import Optional
from pydantic import HttpUrl
from dataclasses import dataclass

@dataclass
class IssueContent:
    issue_id: str
    summary: str
    description: str

class JiraIssuesClient:
    def __init__(self, issues_user: str, issues_api_key: str, httpx_client: httpx.Client) -> None:
        self.issues_user = issues_user
        self.issues_api_key = issues_api_key
        self.httpx_client = httpx_client

    def get_issue_content(self, issues_url: HttpUrl, issue_id: str) -> Optional[IssueContent]:
        url = f"{issues_url}/{issue_id}"
        response = self.httpx_client.get(
            url,
            auth=(self.issues_user, self.issues_api_key),
            headers={"Accept": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            return IssueContent(
                issue_id=data["key"],
                summary=data["fields"]["summary"],
                description=data["fields"]["description"],
            )
        return None