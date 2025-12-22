import chromadb

def get_chroma_client(workspace_id: str) -> chromadb.PersistentClient:
    if workspace_id not in get_chroma_client.clients:
        client = chromadb.PersistentClient(workspace_id)
        get_chroma_client.clients[workspace_id] = client
    return get_chroma_client.clients[workspace_id]

get_chroma_client.clients = {}