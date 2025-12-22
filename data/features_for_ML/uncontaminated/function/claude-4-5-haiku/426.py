def search_documents(
    query: Annotated[
        str,
        Field(
            description="The search query text used to find relevant information in the indexed documents."
        ),
    ],
) -> SearchDocumentOutput:
    """Searches through previously uploaded and indexed documents using semantic search.

    This function retrieves relevant information from documents that have been processed
    and added to the vector database. It uses semantic similarity to find content that
    best matches the query, rather than simple keyword matching.
    """
    try:
        if not query or not query.strip():
            return SearchDocumentOutput(
                results=[],
                total_results=0,
                query=query,
                error="Query cannot be empty"
            )
        
        # Get the vector store from the state
        vector_store = get_vector_store()
        
        if vector_store is None:
            return SearchDocumentOutput(
                results=[],
                total_results=0,
                query=query,
                error="No documents have been indexed yet. Please upload and index documents first."
            )
        
        # Perform semantic search
        search_results = vector_store.similarity_search_with_score(
            query,
            k=10
        )
        
        # Format results
        formatted_results = []
        for doc, score in search_results:
            formatted_results.append(
                SearchResult(
                    content=doc.page_content,
                    source=doc.metadata.get("source", "Unknown"),
                    score=float(score),
                    metadata=doc.metadata
                )
            )
        
        return SearchDocumentOutput(
            results=formatted_results,
            total_results=len(formatted_results),
            query=query,
            error=None
        )
    
    except Exception as e:
        return SearchDocumentOutput(
            results=[],
            total_results=0,
            query=query,
            error=f"Search failed: {str(e)}"
        )