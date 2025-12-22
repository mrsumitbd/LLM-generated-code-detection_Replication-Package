class DoAccountAuthResponse:
    
    def __init__(self, data: dict) -> None:
        self.success = data.get('success', False)
        self.message = data.get('message', '')
        self.account_id = data.get('account_id', None)
        self.token = data.get('token', '')