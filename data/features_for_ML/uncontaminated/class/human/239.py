from urllib.parse import urljoin
import httpx
from urllib.parse import urlparse
from mcp.shared.auth import OAuthClientInformationFull
from nat.plugins.mcp.auth.auth_provider_config import MCPOAuth2ProviderConfig
from mcp.shared.auth import OAuthClientMetadata

class DynamicClientRegistration:
    """Dynamic client registration utility."""

    def __init__(self, config: MCPOAuth2ProviderConfig):
        self.config = config

    def _authorization_base_url(self) -> str:
        """Get the authorization base URL from the MCP server URL."""
        p = urlparse(str(self.config.server_url))
        return f"{p.scheme}://{p.netloc}"

    async def register(self, endpoints: OAuth2Endpoints, scopes: list[str] | None) -> OAuth2Credentials:
        """Register an OAuth2 client with the Authorization Server using OIDC client registration."""
        # Fallback to /register if metadata didn't provide an endpoint
        registration_url = (str(endpoints.registration_url) if endpoints.registration_url else urljoin(
            self._authorization_base_url(), "/register"))

        metadata = OAuthClientMetadata(
            redirect_uris=[self.config.redirect_uri],
            token_endpoint_auth_method=(getattr(self.config, "token_endpoint_auth_method", None)
                                        or "client_secret_post"),
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope=" ".join(scopes) if scopes else None,
            client_name=self.config.client_name or None,
        )
        payload = metadata.model_dump(by_alias=True, mode="json", exclude_none=True)

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                registration_url,
                json=payload,
                headers={
                    "Content-Type": "application/json", "Accept": "application/json"
                },
            )
            resp.raise_for_status()
            body = await resp.aread()

        try:
            info = OAuthClientInformationFull.model_validate_json(body)
        except Exception as e:
            raise RuntimeError(
                f"Registration response was not valid OAuthClientInformation from {registration_url}") from e

        if not info.client_id:
            raise RuntimeError("No client_id received from registration")

        logger.info("Successfully registered OAuth2 client: %s", info.client_id)
        return OAuth2Credentials(client_id=info.client_id, client_secret=info.client_secret)