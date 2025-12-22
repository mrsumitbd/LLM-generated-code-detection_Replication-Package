import requests
import time
from simkl_mps.credentials import get_env_file_path
from simkl_mps.credentials import get_env_file_path
import time
import requests
import webbrowser
from simkl_mps.credentials import get_env_file_path

def pin_auth_flow(client_id, redirect_uri="urn:ietf:wg:oauth:2.0:oob"):
    """
    Implements the OAuth 2.0 device authorization flow for Simkl authentication.
    
    Args:
        client_id (str): Simkl API client ID
        redirect_uri (str, optional): OAuth redirect URI. Defaults to device flow URI.
        
    Returns:
        str | None: The access token if authentication succeeds, None otherwise.
    """
    import time
    import requests
    import webbrowser
    from pathlib import Path
    from simkl_mps.credentials import get_env_file_path
    
    logger.info("Starting Simkl PIN authentication flow")
    
    if not is_internet_connected():
        logger.error("Cannot start authentication flow: no internet connection")
        print("[ERROR] No internet connection detected. Please check your connection and try again.")
        return None
    
    # Step 1: Request device code
    try:
        headers = _add_user_agent({"Content-Type": "application/json"})
        resp = requests.get(
            f"{SIMKL_API_BASE_URL}/oauth/pin",
            params={"client_id": client_id, "redirect": redirect_uri},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to initiate PIN auth: {e}", exc_info=True)
        print("[ERROR] Could not contact Simkl for authentication. Please check your internet connection and try again.")
        return None
    
    # Extract authentication parameters
    user_code = data["user_code"]
    verification_url = data["verification_url"]
    expires_in = data.get("expires_in", 900)  # Default to 15 minutes if not provided
    pin_url = f"https://simkl.com/pin/{user_code}"
    interval = data.get("interval", 5)  # Default poll interval of 5 seconds
    
    # Display authentication instructions
    print("\n=== Simkl Authentication ===")
    print(f"1. We've opened your browser to: {pin_url}")
    print(f"   (If it didn't open, copy and paste this URL into your browser.)")
    print(f"2. Or go to: {verification_url} and enter the code: {user_code}")
    print(f"   (Code: {user_code})")
    print(f"   (You have {expires_in//60} minutes to complete authentication.)\n")
    
    # Open browser for user convenience
    try:
        # Use https:// protocol explicitly to avoid unknown protocol errors
        webbrowser.open(f"https://simkl.com/pin/{user_code}")
    except Exception as e:
        logger.warning(f"Failed to open browser: {e}")
        # Continue anyway, as user can manually navigate
    
    print("Waiting for you to authorize this application...")
    
    # Step 2: Poll for access token with adaptive backoff
    start_time = time.time()
    poll_headers = _add_user_agent({"Content-Type": "application/json"})
    current_interval = interval
    timeout_warning_shown = False
    
    while time.time() - start_time < expires_in:
        # Show a reminder halfway through the expiration time
        elapsed = time.time() - start_time
        if elapsed > (expires_in / 2) and not timeout_warning_shown:
            remaining_mins = int((expires_in - elapsed) / 60)
            print(f"\n[!] Reminder: You have about {remaining_mins} minutes left to complete authentication.")
            timeout_warning_shown = True
        
        try:
            poll = requests.get(
                f"{SIMKL_API_BASE_URL}/oauth/pin/{user_code}",
                params={"client_id": client_id},
                headers=poll_headers,
                timeout=10
            )
            
            if poll.status_code != 200:
                logger.warning(f"Pin verification returned status {poll.status_code}, retrying...")
                time.sleep(current_interval)
                continue
                
            result = poll.json()
            
            if result.get("result") == "OK":
                access_token = result.get("access_token")
                if access_token:
                    # Success! Save the token
                    print("\n[✓] Authentication successful!")
                    
                    # Get the user ID before saving
                    user_id = None
                    try:
                        print("Retrieving your Simkl user ID...")
                        # Try to get user ID from account endpoint first (more reliable)
                        auth_headers = {
                            'Content-Type': 'application/json',
                            'simkl-api-key': client_id,
                            'Authorization': f'Bearer {access_token}',
                            'Accept': 'application/json'
                        }
                        auth_headers = _add_user_agent(auth_headers)
                        
                        account_resp = requests.get(
                            f"{SIMKL_API_BASE_URL}/users/account", 
                            headers=auth_headers,
                            timeout=10
                        )
                        
                        if account_resp.status_code == 200:
                            account_data = account_resp.json()
                            user_id = account_data.get('id')
                            logger.info(f"Retrieved user ID during authentication: {user_id}")
                            print(f"[✓] Found your Simkl user ID: {user_id}")
                        
                        # If account endpoint failed, try settings
                        if not user_id:
                            settings = get_user_settings(client_id, access_token)
                            if settings and settings.get('user_id'):
                                user_id = settings.get('user_id')
                                logger.info(f"Retrieved user ID from settings: {user_id}")
                                print(f"[✓] Found your Simkl user ID: {user_id}")
                    except Exception as e:
                        logger.warning(f"Failed to retrieve user ID during authentication: {e}")
                        print("[!] Warning: Could not retrieve your Simkl user ID - some features may be limited.")
                    
                    # Save token (and user ID if available) to .env file
                    env_path = get_env_file_path()
                    if not _save_access_token(env_path, access_token, user_id):
                        print("[!] Warning: Couldn't save credentials to file, but you can still use them for this session.")
                    else:
                        print(f"[✓] Credentials saved to: {env_path}\n")
                    
                    # Important: After success, navigate the user back to Simkl main page to complete the experience
                    try:
                        webbrowser.open("https://simkl.com/")
                    except Exception as e:
                        logger.warning(f"Failed to open browser after authentication: {e}")
                    
                    # Validate the token works
                    if _validate_access_token(client_id, access_token):
                        logger.info("Access token validated successfully")
                        return access_token
                    else:
                        logger.error("Access token validation failed")
                        print("[ERROR] Authentication completed but token validation failed. Please try again.")
                        return None
                        
            elif result.get("result") == "KO":
                msg = result.get("message", "")
                if msg == "Authorization pending":
                    # Normal state while waiting for user
                    time.sleep(current_interval)
                elif msg == "Slow down":
                    # API rate limiting, increase interval
                    logger.warning("Received 'Slow down' response, increasing polling interval")
                    current_interval = min(current_interval * 2, 30)  # Max 30 seconds
                    time.sleep(current_interval)
                else:
                    logger.error(f"Authentication failed: {msg}")
                    print(f"[ERROR] Authentication failed: {msg}")
                    return None
            else:
                time.sleep(current_interval)
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Network error during polling: {e}")
            # Implement exponential backoff for connection issues
            current_interval = min(current_interval * 1.5, 20)
            time.sleep(current_interval)
    
    print("[ERROR] Authentication timed out. Please try again.")
    return None