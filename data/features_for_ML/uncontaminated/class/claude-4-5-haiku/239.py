class DynamicClientRegistration:
    """Dynamic client registration utility."""

    def __init__(self, config: MCPOAuth2ProviderConfig):
        self.config = config

    def _authorization_base_url(self) -> str:
        return self.config.authorization_endpoint