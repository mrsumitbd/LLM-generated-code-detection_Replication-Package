import chromadb
from chromadb.config import Settings

_chroma_clients = {}

def get_chroma_client(workspace_id: str) -> chromadb.PersistentClient:
    """
    Gets or initializes a persistent ChromaDB client for the given workspace_id.
    Clients are cached globally.
    """
    if workspace_id in _chroma_clients:
        return _chroma_clients[workspace_id]
    else:
        client = chromadb.PersistentClient(
            settings=Settings(
                chroma_db_impl="deta",
                persist_directory=f"./chroma-data/{workspace_id}"
            )
        )
        _chroma_clients[workspace_id] = client
        return client