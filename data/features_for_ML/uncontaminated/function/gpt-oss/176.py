import requests

def call_ag():
    """
    Calls the agify.io API to predict the age of a default name.
    Returns the JSON response as a dictionary.
    """
    url = "https://api.agify.io"
    params = {"name": "michael"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return {"error": str(exc)}