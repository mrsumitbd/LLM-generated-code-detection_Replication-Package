import os
import threading
from typing import Dict

import chromadb
from chromadb import PersistentClient

# Global cache for clients
_client_cache: Dict[str, PersistentClient] = {}
_cache_lock = threading.Lock()


def get_chroma_client(workspace_id: str) -> PersistentClient:
    """
    Gets or initializes a persistent ChromaDB client for the given workspace_id.
    Clients are cached globally.
    """
    # Normalise workspace_id to a safe directory name
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in workspace_id)

    with _cache_lock:
        if safe_id in _client_cache:
            return _client_cache[safe_id]

        # Ensure the directory exists
        base_dir = os.path.join(os.getcwd(), "chroma_data")
        os.makedirs(base_dir, exist_ok=True)
        client_dir = os.path.join(base_dir, f"workspace_{safe_id}")

        # Create the persistent client
        client = PersistentClient(path=client_dir)

        # Cache and return
        _client_cache[safe_id] = client
        return client