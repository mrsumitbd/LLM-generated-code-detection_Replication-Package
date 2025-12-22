def init_config(config: Configuration):
    """
    Initialize the global configuration and create instances of all required modules.

    This function initializes the global variables for the LLM, embedding model,
    file loader, web crawler, vector database, and RAG agents.

    Args:
        config: The Configuration object to use for initialization.
    """
    global llm, embedding_model, file_loader, web_crawler, vector_db, rag_agent
    
    # Initialize LLM based on configuration
    if config.llm_type == "openai":
        llm = OpenAI(
            api_key=config.openai_api_key,
            model=config.llm_model,
            temperature=config.temperature
        )
    elif config.llm_type == "anthropic":
        llm = Anthropic(
            api_key=config.anthropic_api_key,
            model=config.llm_model,
            temperature=config.temperature
        )
    else:
        raise ValueError(f"Unsupported LLM type: {config.llm_type}")
    
    # Initialize embedding model
    if config.embedding_type == "openai":
        embedding_model = OpenAIEmbedding(
            api_key=config.openai_api_key,
            model=config.embedding_model
        )
    elif config.embedding_type == "huggingface":
        embedding_model = HuggingFaceEmbedding(
            model_name=config.embedding_model
        )
    else:
        raise ValueError(f"Unsupported embedding type: {config.embedding_type}")
    
    # Initialize file loader
    file_loader = FileLoader(
        supported_formats=config.supported_file_formats,
        max_file_size=config.max_file_size
    )
    
    # Initialize web crawler
    web_crawler = WebCrawler(
        timeout=config.crawler_timeout,
        max_pages=config.max_pages_to_crawl,
        user_agent=config.user_agent
    )
    
    # Initialize vector database
    vector_db = VectorDatabase(
        db_type=config.vector_db_type,
        embedding_model=embedding_model,
        db_path=config.vector_db_path,
        dimension=config.embedding_dimension
    )
    
    # Initialize RAG agent
    rag_agent = RAGAgent(
        llm=llm,
        embedding_model=embedding_model,
        vector_db=vector_db,
        file_loader=file_loader,
        web_crawler=web_crawler,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        top_k=config.top_k_results
    )