def inspect_embeddings(app: Application):
    """
    Inspect the embeddings object and print detailed information.
    
    Args:
        app: txtai Application instance
    """
    embeddings = app.embeddings
    print(f"Embeddings Model: {embeddings.model}")
    print(f"Embeddings Dimensions: {embeddings.dimensions}")
    print(f"Embeddings Device: {embeddings.device}")
    print(f"Embeddings Batch Size: {embeddings.batch_size}")
    print(f"Embeddings Normalize: {embeddings.normalize}")
    print(f"Embeddings Pooling: {embeddings.pooling}")