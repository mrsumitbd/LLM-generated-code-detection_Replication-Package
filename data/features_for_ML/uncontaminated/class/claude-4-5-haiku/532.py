class ModelProviderConfig:

    def __init__(self, prefix: str, provider: str, base_url: str, env_var: str):
        self.prefix = prefix
        self.provider = provider
        self.base_url = base_url
        self.env_var = env_var

    def configure(self, model: str, kwargs: Dict[str, Any]) -> None:
        kwargs['model'] = f"{self.prefix}{model}"
        kwargs['base_url'] = self.base_url
        if self.env_var:
            import os
            api_key = os.getenv(self.env_var)
            if api_key:
                kwargs['api_key'] = api_key