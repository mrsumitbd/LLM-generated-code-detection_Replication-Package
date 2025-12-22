def search_vectors(index, query_vector, k=1):
    """Search for the k most similar vectors to the query vector
    
    Args:
        index: The FAISS index
        query_vector: The query vector (numpy array or list)
        k: Number of results to return (default: 1)
        
    Returns:
        tuple: (indices, distances) where:
            - indices is a list of positions in the index
            - distances is a list of the corresponding distances
    """
    import numpy as np
    
    # Convert query_vector to numpy array if it's a list
    if isinstance(query_vector, list):
        query_vector = np.array(query_vector)
    
    # Ensure query_vector is 2D (FAISS expects 2D arrays)
    if query_vector.ndim == 1:
        query_vector = query_vector.reshape(1, -1)
    
    # Ensure the dtype is float32 (FAISS standard)
    query_vector = query_vector.astype(np.float32)
    
    # Search the index
    distances, indices = index.search(query_vector, k)
    
    # Return as lists (flatten from 2D to 1D since we have only one query)
    return indices[0].tolist(), distances[0].tolist()