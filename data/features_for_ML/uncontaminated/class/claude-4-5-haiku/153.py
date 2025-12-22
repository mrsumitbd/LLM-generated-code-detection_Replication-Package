import anthropic
import json
import re


class JiraTool:

    def __init__(self, domain: str, project_key: str, ticket_type: str):
        self.domain = domain
        self.project_key = project_key
        self.ticket_type = ticket_type
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def create_ticket(self, summary: str, description: str) -> dict:
        """Create a Jira ticket using Claude with tool use."""
        tools = [
            {
                "name": "create_jira_ticket",
                "description": "Creates a new Jira ticket with the specified details",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "The summary/title of the ticket"
                        },
                        "description": {
                            "type": "string",
                            "description": "The detailed description of the ticket"
                        },
                        "project_key": {
                            "type": "string",
                            "description": "The Jira project key"
                        },
                        "ticket_type": {
                            "type": "string",
                            "description": "The type of ticket (e.g., Bug, Task, Story)"
                        }
                    },
                    "required": ["summary", "description", "project_key", "ticket_type"]
                }
            }
        ]

        messages = [
            {
                "role": "user",
                "content": f"Create a Jira ticket with the following details:\nSummary: {summary}\nDescription: {description}\nProject Key: {self.project_key}\nTicket Type: {self.ticket_type}"
            }
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Process the response
        ticket_data = {
            "summary": summary,
            "description": description,
            "project_key": self.project_key,
            "ticket_type": self.ticket_type,
            "domain": self.domain
        }

        # Check if Claude used the tool
        for content_block in response.content:
            if content_block.type == "tool_use":
                # Extract the tool input
                tool_input = content_block.input
                ticket_data.update(tool_input)

        return ticket_data

    def search_tickets(self, query: str) -> list:
        """Search for Jira tickets using Claude with tool use."""
        tools = [
            {
                "name": "search_jira_tickets",
                "description": "Searches for Jira tickets matching the given query",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query (JQL or text search)"
                        },
                        "project_key": {
                            "type": "string",
                            "description": "The Jira project key to search in"
                        }
                    },
                    "required": ["query", "project_key"]
                }
            }
        ]

        messages = [
            {
                "role": "user",
                "content": f"Search for Jira tickets in project {self.project_key} with the following query: {query}"
            }
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Process the response
        results = []
        for content_block in response.content:
            if content_block.type == "tool_use":
                # Simulate search results
                results.append({
                    "query": query,
                    "project_key": self.project_key,
                    "domain": self.domain,
                    "tool_used": content_block.name
                })

        return results

    def update_ticket(self, ticket_id: str, updates: dict) -> dict:
        """Update a Jira ticket using Claude with tool use."""
        tools = [
            {
                "name": "update_jira_ticket",
                "description": "Updates an existing Jira ticket with the specified changes",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ID of the ticket to update"
                        },
                        "updates": {
                            "type": "object",
                            "description": "The fields to update and their new values"
                        }
                    },
                    "required": ["ticket_id", "updates"]
                }
            }
        ]

        updates_str = json.dumps(updates)
        messages = [
            {
                "role": "user",
                "content": f"Update Jira ticket {ticket_id} with the following changes: {updates_str}"
            }
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Process the response
        result = {
            "ticket_id": ticket_id,
            "updates": updates,
            "project_key": self.project_key,
            "domain": self.domain
        }

        for content_block in response.content:
            if content_block.type == "tool_use":
                result["tool_used"] = content_block.name

        return result

    def get_ticket_details(self, ticket_id: str) -> dict:
        """Get details of a specific Jira ticket using Claude with tool use."""
        tools = [
            {
                "name": "get_jira_ticket_details",
                "description": "Retrieves detailed information about a specific Jira ticket",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ID of the ticket to retrieve"
                        },
                        "project_key": {
                            "type": "string",
                            "description": "The Jira project key"
                        }
                    },
                    "required": ["ticket_id", "project_key"]
                }
            }
        ]

        messages = [
            {
                "role": "user",
                "content": f"Get the details for Jira ticket {ticket_id} in project {self.project_key}"
            }
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Process the response
        ticket_details = {
            "ticket_id": ticket_id,
            "project_key": self.project_key,
            "domain": self.domain
        }

        for content_block in response.content:
            if content_block.type == "tool_use":
                ticket_details.update(content_block.input)

        return ticket_details

    def add_comment(self, ticket_id: str, comment: str) -> dict:
        """Add a comment to a Jira ticket using Claude with tool use."""
        tools = [
            {
                "name": "add_jira_comment",
                "description": "Adds a comment to an existing Jira ticket",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ID of the ticket to comment on"
                        },
                        "comment": {
                            "type": "string",
                            "description": "The comment text to add"
                        }
                    },
                    "required": ["ticket_id", "comment"]
                }
            }
        ]

        messages = [
            {
                "role": "user",
                "content": f"Add the following comment to Jira ticket {ticket_id}: {comment}"
            }
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Process the response
        result = {
            "ticket_id": ticket_id,
            "comment": comment,
            "project_key": self.project_key,
            "domain": self.domain
        }

        for content_block in response.content:
            if content_block.type == "tool_use":
                result["tool_used"] = content_block.name

        return result


if __name__ == "__main__":
    # Example usage
    jira_tool = JiraTool(
        domain="https://example.atlassian.net",
        project_key="PROJ",
        ticket_type="Bug"
    )

    # Create a ticket
    ticket = jira_tool.create_ticket(
        summary="Test ticket",
        description="This is a test ticket"
    )
    print("Created ticket:", ticket)

    # Search for tickets
    results = jira_tool.search_tickets("status = Open")
    print("Search results:", results)

    # Get ticket details
    details = jira_tool.get_ticket_details("PROJ-123")
    print("Ticket details:", details)

    # Update a ticket
    updates = jira_tool.update_ticket(
        "PROJ-123",
        {"status": "In Progress", "assignee": "user@example.com"}
    )
    print("Updated ticket:", updates)

    # Add a comment
    comment = jira_tool.add_comment(
        "PROJ-123",
        "This is a test comment"
    )
    print("Added comment:", comment)