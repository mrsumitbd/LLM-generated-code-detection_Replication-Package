from deepsearcher.agent import ChainOfRAG, DeepSearch, NaiveRAG
from deepsearcher.agent.rag_router import RAGRouter

def init_config(config: Configuration):
    """
    Initialize the global configuration and create instances of all required modules.

    This function initializes the global variables for the LLM, embedding model,
    file loader, web crawler, vector database, and RAG agents.

    Args:
        config: The Configuration object to use for initialization.
    """
    global \
        module_factory, \
        llm, \
        embedding_model, \
        file_loader, \
        vector_db, \
        web_crawler, \
        default_searcher, \
        naive_rag
    module_factory = ModuleFactory(config)
    llm = module_factory.create_llm()
    embedding_model = module_factory.create_embedding()
    file_loader = module_factory.create_file_loader()
    web_crawler = module_factory.create_web_crawler()
    vector_db = module_factory.create_vector_db()

    default_searcher = RAGRouter(
        llm=llm,
        rag_agents=[
            DeepSearch(
                llm=llm,
                embedding_model=embedding_model,
                vector_db=vector_db,
                max_iter=config.query_settings["max_iter"],
                route_collection=True,
                text_window_splitter=True,
            ),
            ChainOfRAG(
                llm=llm,
                embedding_model=embedding_model,
                vector_db=vector_db,
                max_iter=config.query_settings["max_iter"],
                route_collection=True,
                text_window_splitter=True,
            ),
        ],
    )
    naive_rag = NaiveRAG(
        llm=llm,
        embedding_model=embedding_model,
        vector_db=vector_db,
        top_k=10,
        route_collection=True,
        text_window_splitter=True,
    )