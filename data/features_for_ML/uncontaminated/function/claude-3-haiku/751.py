import requests
import json

def api_docs_put(item: str) -> dict:
    url = "https://api.example.com/docs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_access_token"
    }
    data = {
        "item": item
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}