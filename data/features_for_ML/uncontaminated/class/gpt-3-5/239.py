from typing import Optional

class DynamicClientRegistration:
    """Dynamic client registration utility."""

    def __init__(self, config: MCPOAuth2ProviderConfig):
        self.config = config

    def _authorization_base_url(self) -> str:
        return self.config.authorization_base_url

class MCPOAuth2ProviderConfig:
    def __init__(self, authorization_base_url: str):
        self.authorization_base_url = authorization_base_url

# Example usage:
config = MCPOAuth2ProviderConfig(authorization_base_url='https://example.com/oauth2/authorize')
client_registration = DynamicClientRegistration(config)
print(client_registration._authorization_base_url())