def get_basic_auth_token(self):
    import base64
    auth_token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
    return f"Basic {auth_token}"