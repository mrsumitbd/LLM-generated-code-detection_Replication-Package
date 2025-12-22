import os
from typing import Any, Dict


class ModelProviderConfig:
    """
    Configuration helper for model providers.

    Parameters
    ----------
    prefix : str
        Prefix to use for environment variable names (e.g. "OPENAI_").
    provider : str
        Name of the provider (e.g. "openai").
    base_url : str
        Base URL for the provider's API.
    env_var : str
        Name of the environment variable that holds the API key.
    """

    def __init__(self, prefix: str, provider: str, base_url: str, env_var: str):
        self.prefix = prefix
        self.provider = provider
        self.base_url = base_url
        self.env_var = env_var

    def configure(self, model: str, kwargs: Dict[str, Any]) -> None:
        """
        Populate the kwargs dictionary with the necessary configuration
        for the provider.

        Parameters
        ----------
        model : str
            The model name to use.
        kwargs : dict
            Dictionary to be updated with provider configuration.
        """
        # Basic model and provider info
        kwargs["model"] = model
        kwargs["provider"] = self.provider
        kwargs["base_url"] = self.base_url

        # Retrieve API key from environment
        api_key = os.getenv(self.env_var)
        if api_key is None:
            raise ValueError(
                f"Environment variable '{self.env_var}' is not set. "
                f"Please set it to the API key for {self.provider}."
            )
        kwargs["api_key"] = api_key

        # Optional: add prefix for downstream usage
        kwargs["prefix"] = self.prefix