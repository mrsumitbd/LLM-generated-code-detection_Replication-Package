class JiraIssuesClient:

    def __init__(self, issues_user: str, issues_api_key: str, httpx_client: httpx.Client) -> None:
        self.issues_user = issues_user
        self.issues_api_key = issues_api_key
        self.httpx_client = httpx_client

    def get_issue_content(self, issues_url: HttpUrl, issue_id: str) -> IssueContent | None:
        url = f"{issues_url}/rest/api/3/issues/{issue_id}"
        
        try:
            response = self.httpx_client.get(
                url,
                auth=(self.issues_user, self.issues_api_key),
                timeout=30.0
            )
            response.raise_for_status()
        except httpx.HTTPError:
            return None
        
        data = response.json()
        
        fields = data.get("fields", {})
        summary = fields.get("summary", "")
        description = fields.get("description", "")
        
        description_text = ""
        if description:
            if isinstance(description, dict):
                description_text = self._extract_text_from_adf(description)
            else:
                description_text = str(description)
        
        return IssueContent(
            id=data.get("key", issue_id),
            summary=summary,
            description=description_text
        )
    
    def _extract_text_from_adf(self, adf: dict) -> str:
        """Extract plain text from Atlassian Document Format"""
        text_parts = []
        
        def extract_from_node(node):
            if isinstance(node, dict):
                if "text" in node:
                    text_parts.append(node["text"])
                if "content" in node:
                    for child in node["content"]:
                        extract_from_node(child)
            elif isinstance(node, list):
                for item in node:
                    extract_from_node(item)
        
        extract_from_node(adf)
        return "".join(text_parts)