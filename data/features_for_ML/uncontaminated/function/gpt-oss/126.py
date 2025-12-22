import time
import requests

def pin_auth_flow(client_id, redirect_uri="urn:ietf:wg:oauth:2.0:oob"):
    """
    Implements the OAuth 2.0 device authorization flow for Simkl authentication.

    Args:
        client_id (str): Simkl API client ID
        redirect_uri (str, optional): OAuth redirect URI. Defaults to device flow URI.

    Returns:
        str | None: The access token if authentication succeeds, None otherwise.
    """
    # Endpoint URLs
    device_code_url = "https://api.simkl.com/oauth/device/code"
    token_url = "https://api.simkl.com/oauth/token"

    # Step 1: Request device and user codes
    try:
        resp = requests.post(
            device_code_url,
            data={
                "client_id": client_id,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
    except Exception:
        return None

    data = resp.json()
    device_code = data.get("device_code")
    user_code = data.get("user_code")
    verification_uri = data.get("verification_uri")
    expires_in = data.get("expires_in", 600)
    interval = data.get("interval", 5)

    if not all([device_code, user_code, verification_uri]):
        return None

    # Inform user
    print(f"Please visit {verification_uri} and enter the code: {user_code}")

    # Step 2: Poll for token
    start_time = time.time()
    while time.time() - start_time < expires_in:
        try:
            token_resp = requests.post(
                token_url,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                    "client_id": client_id,
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
            if token_resp.status_code == 200:
                token_data = token_resp.json()
                return token_data.get("access_token")
            elif token_resp.status_code == 400:
                err = token_resp.json().get("error")
                if err in ("authorization_pending", "slow_down"):
                    # Continue polling
                    pass
                else:
                    # Other errors mean failure
                    break
            else:
                # Unexpected status
                break
        except Exception:
            break

        time.sleep(interval)

    return None