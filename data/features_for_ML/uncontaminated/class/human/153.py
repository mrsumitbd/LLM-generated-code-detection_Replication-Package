import os
import httpx

class JiraTool:

    def __init__(self, domain: str, project_key: str, ticket_type: str):
        self.domain = domain
        self.userid = os.getenv("JIRA_USERID")
        self.token = os.getenv("JIRA_TOKEN")
        self.ticket_type = ticket_type
        self.project_key = project_key
        self.url = f"{self.domain}/rest/api/2/issue"

    async def get_priority_name(self, priority: str):
        if priority == 'P0':
            return priority + " - Must have"
        if priority == 'P1':
            return priority + " - Should have"
        if priority == 'P2':
            return priority + " - Nice to have"

    async def create_epic(self, client: httpx.AsyncClient, ticket_data: dict) -> str:
        """
        Creates a Jira Epic and returns the epic key (e.g. "PROJ-123").
        """
        title = ticket_data.get("name", "Untitled")
        epic_description = ticket_data.get("description", "")
        logger.debug("Creating Epic in Jira: %s", title)
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": epic_description,
                "issuetype": {
                    "name": "Epic"
                },
                "customfield_10006": title
            }
        }
        try:
            r = await client.post(
                self.url,
                json=payload,
                auth=(self.userid, self.token),
                headers={"Content-Type": "application/json"},
            )

            r.raise_for_status()  # Raise error for 4xx/5xx
        except httpx.HTTPStatusError as err:
            return {"error": f"HTTP error: {err.response.status_code}", "details": err.response.text}
        except httpx.RequestError as err:
            return {
                "error": "Request error",
                "message": str(err),
                "request_url": str(err.request.url) if err.request else "N/A"
            }

        data = r.json()
        return data["key"], data["self"]

    async def create_task(self, client: httpx.AsyncClient, ticket_data: dict):
        """
        Creates a Task Type with assigned priority and story points.
        """
        title = ticket_data.get("title", "Untitled Story")
        description = ticket_data.get("description", "")
        priority = ticket_data.get("priority", "")
        story_points = ticket_data.get("storypoints", "")
        logger.debug("Creating Tasks in Jira: %s for priority %s with story point %s", title, priority, story_points)
        priority_name = await self.get_priority_name(priority)
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": description,
                "issuetype": {
                    "name": "Task"
                },
                "priority": {
                    "name": priority_name
                }
            }
        }
        try:
            r = await client.post(
                self.url,
                json=payload,
                auth=(self.userid, self.token),
                headers={"Content-Type": "application/json"},
            )

            r.raise_for_status()  # Raise error for 4xx/5xx
        except httpx.HTTPStatusError as err:
            return {"error": f"HTTP error: {err.response.status_code}", "details": err.response.text}
        except httpx.RequestError as err:
            return {
                "error": "Request error",
                "message": str(err),
                "request_url": str(err.request.url) if err.request else "N/A"
            }
        data = r.json()
        return data["key"], data["self"]

    async def create_bug(self, client: httpx.AsyncClient, ticket_data: dict):
        """
        Creates a Bug Type with assigned priority and story points.
        """
        title = ticket_data.get("title", "Untitled Story")
        description = ticket_data.get("description", "")
        priority = ticket_data.get("priority", "")
        story_points = ticket_data.get("storypoints", "")
        logger.debug("Creating Tasks in Jira: %s for priority %s with story point %s", title, priority, story_points)
        priority_name = await self.get_priority_name(priority)
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": description,
                "issuetype": {
                    "name": "Bug"
                },
                "priority": {
                    "name": priority_name
                },
                "customfield_10002":
                    int(story_points)  # Update with the desired story points
            }
        }
        try:
            r = await client.post(
                self.url,
                json=payload,
                auth=(self.userid, self.token),
                headers={"Content-Type": "application/json"},
            )

            r.raise_for_status()  # Raise error for 4xx/5xx
        except httpx.HTTPStatusError as err:
            return {"error": f"HTTP error: {err.response.status_code}", "details": err.response.text}
        except httpx.RequestError as err:
            return {
                "error": "Request error",
                "message": str(err),
                "request_url": str(err.request.url) if err.request else "N/A"
            }
        data = r.json()
        return data["key"], data["self"]

    async def create_feature(self, client: httpx.AsyncClient, ticket_data: dict):
        """
        Creates a Feature Type with assigned priority and story points.
        """
        title = ticket_data.get("title", "Untitled Story")
        description = ticket_data.get("description", "")
        priority = ticket_data.get("priority", "")
        story_points = ticket_data.get("storypoints", "")
        logger.debug("Creating Tasks in Jira: %s for priority %s with story point %s", title, priority, story_points)
        priority_name = await self.get_priority_name(priority)
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": description,
                "issuetype": {
                    "name": "New Feature"
                },
                "priority": {
                    "name": priority_name
                },
                "customfield_10002":
                    int(story_points)  # Update with the desired story points
            }
        }
        try:
            r = await client.post(
                self.url,
                json=payload,
                auth=(self.userid, self.token),
                headers={"Content-Type": "application/json"},
            )

            r.raise_for_status()  # Raise error for 4xx/5xx
        except httpx.HTTPStatusError as err:
            return {"error": f"HTTP error: {err.response.status_code}", "details": err.response.text}
        except httpx.RequestError as err:
            return {
                "error": "Request error",
                "message": str(err),
                "request_url": str(err.request.url) if err.request else "N/A"
            }
        data = r.json()
        return data["key"], data["self"]