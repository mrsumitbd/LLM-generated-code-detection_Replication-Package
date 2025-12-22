import chromadb
from pathlib import Path

_chroma_clients = {}

def get_chroma_client(workspace_id: str) -> chromadb.PersistentClient:
    """
    Gets or initializes a persistent ChromaDB client for the given workspace_id.
    Clients are cached globally.
    """
    if workspace_id not in _chroma_clients:
        db_path = Path.home() / ".chroma" / workspace_id
        db_path.mkdir(parents=True, exist_ok=True)
        _chroma_clients[workspace_id] = chromadb.PersistentClient(path=str(db_path))
    
    return _chroma_clients[workspace_id]