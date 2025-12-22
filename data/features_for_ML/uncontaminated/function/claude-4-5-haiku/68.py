def _default_session_api_keys():
    # Legacy fallback for compability with old runtime API
    import os
    from typing import Dict, Any
    
    api_keys: Dict[str, Any] = {}
    
    # Check for common environment variables that might contain API keys
    env_vars = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'GOOGLE_API_KEY',
        'HUGGINGFACE_API_KEY',
        'COHERE_API_KEY',
        'REPLICATE_API_KEY',
        'TOGETHER_API_KEY',
        'MISTRAL_API_KEY',
        'GROQ_API_KEY',
        'PERPLEXITY_API_KEY',
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # Convert environment variable name to a key name
            key_name = var.replace('_API_KEY', '').lower()
            api_keys[key_name] = value
    
    return api_keys