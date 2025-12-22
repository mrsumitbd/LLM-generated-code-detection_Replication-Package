def init_config(config: Configuration):
    """
    Initialize the global configuration and create instances of all required modules.

    This function initializes the global variables for the LLM, embedding model,
    file loader, web crawler, vector database, and RAG agents.

    Args:
        config: The Configuration object to use for initialization.
    """
    # Import the global variables that will be set by this function.
    # They are expected to be defined at module level in the same package.
    global llm, embedding_model, file_loader, web_crawler, vector_db, rag_agent

    # Helper to fetch a value from the config.  The config object may expose
    # attributes directly or provide a ``get`` method (e.g. a dict‑like API).
    def _get(name: str):
        if hasattr(config, "get"):
            return config.get(name)
        return getattr(config, name, None)

    # Initialise each component.  If the config does not provide a value,
    # the component will be left as ``None``.
    llm = _get("llm")
    embedding_model = _get("embedding_model")
    file_loader = _get("file_loader")
    web_crawler = _get("web_crawler")
    vector_db = _get("vector_db")
    rag_agent = _get("rag_agent")