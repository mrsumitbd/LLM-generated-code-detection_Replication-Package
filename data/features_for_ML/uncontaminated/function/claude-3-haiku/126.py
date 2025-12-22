import requests
import time

def pin_auth_flow(client_id, redirect_uri="urn:ietf:wg:oauth:2.0:oob"):
    """
    Implements the OAuth 2.0 device authorization flow for Simkl authentication.
    
    Args:
        client_id (str): Simkl API client ID
        redirect_uri (str, optional): OAuth redirect URI. Defaults to device flow URI.
        
    Returns:
        str | None: The access token if authentication succeeds, None otherwise.
    """
    # Step 1: Request device and user codes
    url = "https://api.simkl.com/oauth/device"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    response = requests.post(url, params=params)
    data = response.json()
    
    if "error" in data:
        return None
    
    user_code = data["user_code"]
    device_code = data["device_code"]
    interval = data["interval"]
    
    # Step 2: Prompt user to enter the user code
    print(f"Please enter the user code: {user_code}")
    
    # Step 3: Poll for access token
    url = "https://api.simkl.com/oauth/device/token"
    params = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
    }
    
    while True:
        response = requests.post(url, params=params)
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        elif "error" in data:
            if data["error"] == "authorization_pending":
                time.sleep(interval)
                continue
            else:
                return None
        else:
            return None