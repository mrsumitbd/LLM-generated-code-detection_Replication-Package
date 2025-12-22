def init_config(config: Configuration):
    """
    Initialize the global configuration and create instances of all required modules.

    This function initializes the global variables for the LLM, embedding model,
    file loader, web crawler, vector database, and RAG agents.

    Args:
        config: The Configuration object to use for initialization.
    """
    global llm, embedding_model, file_loader, web_crawler, vector_db, rag_agent

    # Initialize the Language Model (LLM)
    llm = create_llm(config.llm_model, config.llm_params)

    # Initialize the Embedding Model
    embedding_model = create_embedding_model(config.embedding_model, config.embedding_params)

    # Initialize the File Loader
    file_loader = create_file_loader(config.file_loader_type, config.file_loader_params)

    # Initialize the Web Crawler
    web_crawler = create_web_crawler(config.web_crawler_type, config.web_crawler_params)

    # Initialize the Vector Database
    vector_db = create_vector_db(config.vector_db_type, config.vector_db_params)

    # Initialize the RAG Agent
    rag_agent = create_rag_agent(config.rag_agent_type, config.rag_agent_params, llm, embedding_model, vector_db)