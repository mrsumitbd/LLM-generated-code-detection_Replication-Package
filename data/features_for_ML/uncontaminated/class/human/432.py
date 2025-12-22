from pydantic import BaseModel, HttpUrl, ValidationError
from lgtm_ai.git_client.schemas import IssueContent
import httpx
from typing import ClassVar

class JiraIssuesClient:
    API_VERSION: ClassVar[int] = 3

    def __init__(self, issues_user: str, issues_api_key: str, httpx_client: httpx.Client) -> None:
        self._issues_user = issues_user
        self._issues_api_key = issues_api_key
        self._httpx_client = httpx_client

    def get_issue_content(self, issues_url: HttpUrl, issue_id: str) -> IssueContent | None:
        """Fetch the content of an issue from the base URL of the issues page.

        Returns None if the issue cannot be fetched or parsed.
        """
        api_url = f"https://{issues_url.host}/rest/api/{self.API_VERSION}/issue/{issue_id}"

        try:
            response = self._httpx_client.get(api_url, auth=(self._issues_user, self._issues_api_key))
            response.raise_for_status()
            jira_issue = _JiraIssueResponse.model_validate(response.json())
            return IssueContent(title=jira_issue.title, description=jira_issue.description_text)
        except httpx.HTTPError:
            logger.error("Error fetching issue content for %s from Jira at %s", issue_id, issues_url.host)
            return None
        except ValidationError as err:
            logger.error("Error parsing issue content for %s from Jira: %s", issue_id, err)
            return None
        except Exception as err:
            logger.error("Unexpected error fetching issue content for %s from Jira: %s", issue_id, err)
            return None