import chromadb
from chromadb.config import Settings as ChromaSettings

def get_chroma_client(workspace_id: str) -> chromadb.PersistentClient:
    """
    Gets or initializes a persistent ChromaDB client for the given workspace_id.
    Clients are cached globally.
    """
    if workspace_id not in _chroma_clients:
        vector_store_path = _get_vector_store_path(workspace_id)
        log.info(f"Initializing ChromaDB client for workspace '{workspace_id}' at path: {vector_store_path}")
        try:
            # Settings for on-disk persistence.
            # allow_reset=True can be useful during development if schema changes.
            client = chromadb.PersistentClient(path=vector_store_path, settings=ChromaSettings(allow_reset=True, anonymized_telemetry=False))
            _chroma_clients[workspace_id] = client
        except Exception as e:
            log.error(f"Failed to initialize ChromaDB client for workspace '{workspace_id}': {e}", exc_info=True)
            raise
    return _chroma_clients[workspace_id]