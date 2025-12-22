def _list_providers(providers: list[ModelProvider]):
    """List all available model providers."""
    if not providers:
        print("No providers available.")
        return
    
    print("Available Model Providers:")
    print("-" * 50)
    
    for provider in providers:
        print(f"  • {provider.name}")
        if hasattr(provider, 'description') and provider.description:
            print(f"    {provider.description}")
        if hasattr(provider, 'models') and provider.models:
            print(f"    Models: {', '.join(provider.models)}")
    
    print("-" * 50)