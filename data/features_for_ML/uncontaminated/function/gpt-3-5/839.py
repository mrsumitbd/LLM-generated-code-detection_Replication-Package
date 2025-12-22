def init_config(config: Configuration):
    global LLM
    global embedding_model
    global file_loader
    global web_crawler
    global vector_database
    global RAG_agents

    LLM = LLMModule(config.llm_config)
    embedding_model = EmbeddingModel(config.embedding_model_config)
    file_loader = FileLoader(config.file_loader_config)
    web_crawler = WebCrawler(config.web_crawler_config)
    vector_database = VectorDatabase(config.vector_database_config)
    RAG_agents = RAGAgents(config.rag_agents_config)