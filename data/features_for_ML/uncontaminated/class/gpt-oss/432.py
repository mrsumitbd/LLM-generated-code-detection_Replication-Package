from __future__ import annotations

import httpx
from typing import Optional

from pydantic import BaseModel, HttpUrl


class IssueContent(BaseModel):
    id: str
    key: str
    summary: Optional[str] = None
    description: Optional[str] = None


class JiraIssuesClient:
    def __init__(self, issues_user: str, issues_api_key: str, httpx_client: httpx.Client) -> None:
        self.issues_user = issues_user
        self.issues_api_key = issues_api_key
        self.httpx_client = httpx_client

    def get_issue_content(self, issues_url: HttpUrl, issue_id: str) -> IssueContent | None:
        """
        Retrieve a Jira issue's content.

        Parameters
        ----------
        issues_url : HttpUrl
            Base URL of the Jira instance (e.g., https://your-domain.atlassian.net).
        issue_id : str
            The issue key or ID to fetch.

        Returns
        -------
        IssueContent | None
            Parsed issue content or None if the request fails.
        """
        # Construct the full API endpoint
        endpoint = f"{issues_url}/rest/api/3/issue/{issue_id}"

        try:
            response = self.httpx_client.get(
                endpoint,
                auth=(self.issues_user, self.issues_api_key),
                timeout=10.0,
            )
            response.raise_for_status()
        except (httpx.HTTPError, httpx.RequestError):
            return None

        data = response.json()

        # Extract fields safely
        fields = data.get("fields", {})
        summary = fields.get("summary")
        description = fields.get("description")

        # Jira may return description as a dict with rich text content
        if isinstance(description, dict):
            # Try to extract plain text from the content array
            content = description.get("content")
            if isinstance(content, list):
                parts = []
                for block in content:
                    if block.get("type") == "paragraph":
                        text_runs = block.get("content", [])
                        for run in text_runs:
                            if run.get("type") == "text":
                                parts.append(run.get("text", ""))
                description = "\n".join(parts) or None

        return IssueContent(
            id=data.get("id", ""),
            key=data.get("key", ""),
            summary=summary,
            description=description,
        )