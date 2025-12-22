def pin_auth_flow(client_id, redirect_uri="urn:ietf:wg:oauth:2.0:oob"):
    import requests

    data = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'device_code'
    }

    response = requests.post('https://api.simkl.com/oauth/pin', data=data)

    if response.status_code == 200:
        device_code = response.json()['device_code']
        user_code = response.json()['user_code']
        verification_url = response.json()['verification_url']
        interval = response.json()['interval']

        print(f"Please visit {verification_url} and enter the code: {user_code}")

        data = {
            'client_id': client_id,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }

        while True:
            response = requests.post('https://api.simkl.com/oauth/token', data=data)
            if response.status_code == 200:
                return response.json()['access_token']
            elif response.status_code == 400 and response.json()['error'] == 'authorization_pending':
                print("Waiting for user authorization...")
                time.sleep(interval)
            else:
                print("Authorization failed.")
                return None
    else:
        print("Authorization request failed.")
        return None