class JiraTool:
    def __init__(self, domain: str, project_key: str, ticket_type: str):
        self.domain = domain
        self.project_key = project_key
        self.ticket_type = ticket_type
        self.session = None

    def login(self, username: str, password: str):
        import requests
        from requests.auth import HTTPBasicAuth

        auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = auth

    def create_ticket(self, summary: str, description: str, assignee: str = None):
        import json

        url = f"https://{self.domain}/rest/api/2/issue"
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": self.ticket_type
                },
                "assignee": {
                    "name": assignee
                }
            }
        }

        response = self.session.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()

    def get_ticket(self, ticket_id: str):
        url = f"https://{self.domain}/rest/api/2/issue/{ticket_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def update_ticket(self, ticket_id: str, fields: dict):
        import json

        url = f"https://{self.domain}/rest/api/2/issue/{ticket_id}"
        payload = {
            "fields": fields
        }
        response = self.session.put(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()

    def close_ticket(self, ticket_id: str):
        url = f"https://{self.domain}/rest/api/2/issue/{ticket_id}/transitions"
        payload = {
            "transition": {
                "id": "5"  # Assuming the 'Done' transition has ID 5
            }
        }
        response = self.session.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()