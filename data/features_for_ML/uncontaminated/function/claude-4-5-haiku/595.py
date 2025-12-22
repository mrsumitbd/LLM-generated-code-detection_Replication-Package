def inspect_embeddings(app: Application):
    """
    Inspect the embeddings object and print detailed information.
    
    Args:
        app: txtai Application instance
    """
    if not hasattr(app, 'embeddings') or app.embeddings is None:
        print("No embeddings object found in the application.")
        return
    
    embeddings = app.embeddings
    
    print("=" * 60)
    print("EMBEDDINGS INSPECTION")
    print("=" * 60)
    
    # Basic information
    print(f"\nEmbeddings Type: {type(embeddings).__name__}")
    print(f"Embeddings Module: {type(embeddings).__module__}")
    
    # Check for common attributes
    if hasattr(embeddings, 'config'):
        print(f"\nConfiguration:")
        config = embeddings.config
        if isinstance(config, dict):
            for key, value in config.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {config}")
    
    # Check for model information
    if hasattr(embeddings, 'model'):
        print(f"\nModel: {embeddings.model}")
    
    if hasattr(embeddings, 'path'):
        print(f"Path: {embeddings.path}")
    
    # Check for dimension
    if hasattr(embeddings, 'dimension'):
        print(f"Dimension: {embeddings.dimension}")
    
    # Check for content
    if hasattr(embeddings, 'content'):
        print(f"Content: {embeddings.content}")
    
    # Check for database
    if hasattr(embeddings, 'database'):
        print(f"Database: {embeddings.database}")
    
    # Check for index
    if hasattr(embeddings, 'index'):
        print(f"Index: {embeddings.index}")
    
    # List all public attributes and methods
    print(f"\nPublic Attributes and Methods:")
    public_members = [member for member in dir(embeddings) if not member.startswith('_')]
    for member in sorted(public_members):
        attr = getattr(embeddings, member)
        if not callable(attr):
            print(f"  {member}: {type(attr).__name__}")
        else:
            print(f"  {member}(): method")
    
    print("\n" + "=" * 60)