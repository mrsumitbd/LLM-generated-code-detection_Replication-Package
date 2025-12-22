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
    query_vector = np.array(query_vector)
    distances, indices = index.search(query_vector.reshape(1, -1), k)
    return indices[0].tolist(), distances[0].tolist()