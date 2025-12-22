def _list_providers(providers: list[ModelProvider]):
    provider_names = [provider.name for provider in providers]
    return provider_names