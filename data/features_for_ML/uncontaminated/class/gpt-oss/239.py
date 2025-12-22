from __future__ import annotations
from typing import Any


class DynamicClientRegistration:
    """Dynamic client registration utility."""

    def __init__(self, config: Any):
        """
        Initialize the dynamic client registration utility.

        Parameters
        ----------
        config : Any
            Configuration object containing OAuth2 provider details.
            Expected to provide at least an `authorization_endpoint` or
            `authorization_url` attribute.
        """
        self.config = config

    def _authorization_base_url(self) -> str:
        """
        Retrieve the base URL for the OAuth2 authorization endpoint.

        Returns
        -------
        str
            The authorization endpoint URL.

        Raises
        ------
        AttributeError
            If the configuration does not provide an authorization endpoint.
        """
        # Prefer the canonical attribute name
        if hasattr(self.config, "authorization_endpoint"):
            return getattr(self.config, "authorization_endpoint")
        # Fallback to an alternative attribute name
        if hasattr(self.config, "authorization_url"):
            return getattr(self.config, "authorization_url")
        # If neither attribute is present, raise an informative error
        raise AttributeError(
            "Configuration object must provide either 'authorization_endpoint' "
            "or 'authorization_url' attribute."
        )