import requests
import json

class _Clients:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.clients = {}

    def refresh(self, tenant_id: int = 1) -> dict:
        url = f"{self.api_url}/clients?tenant_id={tenant_id}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self.clients = {client["uid"]: client for client in response.json()}
        return self.clients

    def register(self, uid: str, client_id: str, tenant_id: int = 1):
        url = f"{self.api_url}/clients"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        data = {
            "uid": uid,
            "client_id": client_id,
            "tenant_id": tenant_id
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        self.clients[uid] = response.json()