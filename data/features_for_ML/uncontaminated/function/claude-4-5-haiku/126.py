def pin_auth_flow(client_id, redirect_uri="urn:ietf:wg:oauth:2.0:oob"):
    """
    Implements the OAuth 2.0 device authorization flow for Simkl authentication.
    
    Args:
        client_id (str): Simkl API client ID
        redirect_uri (str, optional): OAuth redirect URI. Defaults to device flow URI.
        
    Returns:
        str | None: The access token if authentication succeeds, None otherwise.
    """
    import requests
    import time
    
    # Step 1: Request device code
    device_auth_url = "https://api.simkl.com/oauth/device/code"
    device_payload = {
        "client_id": client_id
    }
    
    try:
        device_response = requests.post(device_auth_url, json=device_payload)
        device_response.raise_for_status()
        device_data = device_response.json()
    except requests.RequestException:
        return None
    
    device_code = device_data.get("device_code")
    user_code = device_data.get("user_code")
    verification_url = device_data.get("verification_url")
    expires_in = device_data.get("expires_in", 1800)
    interval = device_data.get("interval", 5)
    
    if not device_code or not user_code:
        return None
    
    # Step 2: Display user code and verification URL
    print(f"Please visit: {verification_url}")
    print(f"Enter code: {user_code}")
    
    # Step 3: Poll for token
    token_url = "https://api.simkl.com/oauth/device/token"
    token_payload = {
        "client_id": client_id,
        "device_code": device_code
    }
    
    start_time = time.time()
    
    while time.time() - start_time < expires_in:
        try:
            token_response = requests.post(token_url, json=token_payload)
            token_response.raise_for_status()
            token_data = token_response.json()
            
            if "access_token" in token_data:
                return token_data["access_token"]
            
            # Check for error responses
            if token_data.get("error") == "authorization_pending":
                time.sleep(interval)
                continue
            elif token_data.get("error") == "slow_down":
                interval += 5
                time.sleep(interval)
                continue
            elif token_data.get("error") in ["expired_token", "access_denied"]:
                return None
                
        except requests.RequestException:
            return None
    
    return None