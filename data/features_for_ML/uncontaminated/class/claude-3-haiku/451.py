class ClientAuthenticator:
    """
    ClientAuthenticator is a callable which validates requests from a client
    application, used to verify /token calls.
    If, during registration, the client requested to be issued a secret, the
    authenticator asserts that /token calls must be authenticated with
    that same token.
    NOTE: clients can opt for no authentication during registration, in which case this
    logic is skipped.
    """

    def __init__(self, provider: OAuthAuthorizationServerProvider[Any, Any, Any]):
        self.provider = provider
        self.client_secrets = {}

    def __call__(self, request: Any) -> bool:
        client_id = request.get("client_id")
        client_secret = request.get("client_secret")

        if client_id in self.client_secrets:
            expected_secret = self.client_secrets[client_id]
            if client_secret != expected_secret:
                return False

        try:
            client = self.provider.get_client(client_id)
            if client.require_client_authentication:
                if client_secret is None:
                    return False
                if not self.provider.validate_client_credentials(client_id, client_secret):
                    return False
        except KeyError:
            return False

        return True

    def register_client(self, client_id: str, client_secret: str = None):
        self.client_secrets[client_id] = client_secret