def inspect_embeddings(app: Application):
    print("Embeddings information:")
    print(f"Number of embeddings: {len(app.embeddings)}")
    print(f"Embedding size: {app.embeddings.size}")
    print(f"Embedding dimension: {app.embeddings.dim}")
    print(f"Embedding type: {type(app.embeddings)}")