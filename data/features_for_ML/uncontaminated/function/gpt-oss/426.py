from typing import Annotated
from pydantic import Field

# Import the output model (assumed to be defined elsewhere in the project)
try:
    from .models import SearchDocumentOutput
except Exception:
    # Fallback definition if the actual model is not available
    from pydantic import BaseModel, Field as PydanticField
    class SearchDocumentOutput(BaseModel):
        results: list[str] = PydanticField(..., description="List of relevant document snippets")

# Vector store imports (adjust according to the actual vector store used)
try:
    from langchain.vectorstores import FAISS
    from langchain.embeddings import OpenAIEmbeddings
except Exception:
    FAISS = None
    OpenAIEmbeddings = None

# Global vector store instance (should be initialized elsewhere in the application)
vector_store = None

def _initialize_vector_store():
    """Initializes the global vector store if not already set."""
    global vector_store
    if vector_store is None:
        if FAISS is None or OpenAIEmbeddings is None:
            raise RuntimeError("Vector store dependencies are not available.")
        embeddings = OpenAIEmbeddings()
        # Load a local FAISS index; adjust the path as needed
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

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
    # Ensure the vector store is ready
    _initialize_vector_store()

    # Perform a similarity search; adjust k as appropriate
    try:
        docs = vector_store.similarity_search(query, k=5)
    except Exception as exc:
        raise RuntimeError(f"Vector store search failed: {exc}") from exc

    # Extract text from the returned documents
    snippets = [doc.page_content for doc in docs]

    return SearchDocumentOutput(results=snippets)