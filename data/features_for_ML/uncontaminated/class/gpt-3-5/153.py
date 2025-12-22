class JiraTool:

    def __init__(self, domain: str, project_key: str, ticket_type: str):
        self.domain = domain
        self.project_key = project_key
        self.ticket_type = ticket_type

    def create_ticket(self, summary: str, description: str):
        print(f"Creating a new {self.ticket_type} ticket in project {self.project_key} on domain {self.domain}")
        print(f"Summary: {summary}")
        print(f"Description: {description}")

    def close_ticket(self, ticket_id: str):
        print(f"Closing {self.ticket_type} ticket with ID {ticket_id} in project {self.project_key} on domain {self.domain}")