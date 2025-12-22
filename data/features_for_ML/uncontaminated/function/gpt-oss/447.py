import numpy as np

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
    if index is None:
        raise ValueError("Index must not be None")

    # Ensure query_vector is a 2‑D float32 array of shape (1, dim)
    q = np.asarray(query_vector, dtype=np.float32)
    if q.ndim == 1:
        q = q.reshape(1, -1)
    elif q.ndim == 2 and q.shape[0] == 1:
        pass
    else:
        raise ValueError("query_vector must be a 1‑D array or a 2‑D array with a single row")

    # Clamp k to the number of vectors in the index
    k = int(k)
    if k <= 0:
        raise ValueError("k must be a positive integer")
    if k > index.ntotal:
        k = index.ntotal

    # Perform the search
    distances, indices = index.search(q, k)

    # Convert to Python lists and return
    return indices[0].tolist(), distances[0].tolist()