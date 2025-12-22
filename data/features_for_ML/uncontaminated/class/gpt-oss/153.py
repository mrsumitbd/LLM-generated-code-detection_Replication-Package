import os
import json
from typing import Any, Dict, List, Optional, Union

import requests
from requests.auth import HTTPBasicAuth


class JiraTool:
    """
    A lightweight wrapper around the Jira REST API.

    Parameters
    ----------
    domain : str
        The Jira instance domain (e.g. "mycompany.atlassian.net").
    project_key : str
        The key of the Jira project to operate on.
    ticket_type : str
        The name of the issue type to create (e.g. "Bug", "Task").
    """

    def __init__(self, domain: str, project_key: str, ticket_type: str):
        self.domain = domain.rstrip("/")
        self.project_key = project_key
        self.ticket_type = ticket_type
        self.base_url = f"https://{self.domain}/rest/api/2"

        # Authentication: look for environment variables
        user = os.getenv("JIRA_USER")
        token = os.getenv("JIRA_TOKEN")
        if user and token:
            self._auth = HTTPBasicAuth(user, token)
        else:
            self._auth = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        if isinstance(data, dict):
            data = json.dumps(data)

        resp = requests.request(
            method,
            url,
            auth=self._auth,
            headers=self._headers(),
            params=params,
            data=data,
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Jira API error {resp.status_code}: {resp.text}"
            ) from exc

        if resp.content:
            return resp.json()
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def create_issue(
        self,
        summary: str,
        description: str,
        *,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new issue in the configured project.

        Returns the full issue representation returned by Jira.
        """
        payload: Dict[str, Any] = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": self.ticket_type},
            }
        }

        if assignee:
            payload["fields"]["assignee"] = {"name": assignee}
        if labels:
            payload["fields"]["labels"] = labels
        if custom_fields:
            payload["fields"].update(custom_fields)

        return self._request("POST", "/issue", data=payload)

    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """
        Retrieve an issue by its key or ID.
        """
        return self._request("GET", f"/issue/{issue_id}")

    def update_issue(
        self,
        issue_id: str,
        fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update fields of an existing issue.

        The `fields` dict should follow Jira's field naming conventions.
        """
        payload = {"fields": fields}
        return self._request("PUT", f"/issue/{issue_id}", data=payload)

    def delete_issue(self, issue_id: str) -> None:
        """
        Delete an issue. No return value.
        """
        self._request("DELETE", f"/issue/{issue_id}")

    def search_issues(
        self,
        jql: str,
        *,
        max_results: int = 50,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for issues using a JQL query.

        Returns a list of issue objects.
        """
        params = {"jql": jql, "maxResults": max_results}
        if fields:
            params["fields"] = ",".join(fields)

        result = self._request("GET", "/search", params=params)
        return result.get("issues", [])

    def get_project_info(self) -> Dict[str, Any]:
        """
        Retrieve metadata about the configured project.
        """
        return self._request("GET", f"/project/{self.project_key}")

    def __repr__(self) -> str:
        return (
            f"<JiraTool domain={self.domain!r} "
            f"project_key={self.project_key!r} "
            f"ticket_type={self.ticket_type!r}>"
        )