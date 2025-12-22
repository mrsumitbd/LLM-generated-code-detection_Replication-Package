class DoAccountAuthResponse:
    def __init__(self, data: dict) -> None:
        self.status = data.get('status', None)
        self.message = data.get('message', None)
        self.account_id = data.get('account_id', None)
        self.access_token = data.get('access_token', None)
        self.refresh_token = data.get('refresh_token', None)
        self.expires_in = data.get('expires_in', None)