def search_vectors(index, query_vector, k=1):
    D, I = index.search(np.array([query_vector]), k)
    return I[0].tolist(), D[0].tolist()