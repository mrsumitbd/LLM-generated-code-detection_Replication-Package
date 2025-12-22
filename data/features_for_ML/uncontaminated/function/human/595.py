import os
from pathlib import Path
from txtai.app import Application

def inspect_embeddings(app: Application):
    """
    Inspect the embeddings object and print detailed information.
    
    Args:
        app: txtai Application instance
    """
    logger.info("--- EMBEDDINGS INSPECTION ---")
    
    if not hasattr(app, 'embeddings') or not app.embeddings:
        logger.error("No embeddings found in application!")
        return
    
    # Basic embeddings info
    logger.info(f"Embeddings path: {app.embeddings.path if hasattr(app.embeddings, 'path') else 'Not set'}")
    logger.info(f"Embeddings dimension: {app.embeddings.dimension if hasattr(app.embeddings, 'dimension') else 'Unknown'}")
    
    # Check if index is initialized
    if hasattr(app.embeddings, 'initialized'):
        logger.info(f"Embeddings initialized: {app.embeddings.initialized}")
    else:
        logger.info("Embeddings initialized status: Unknown")
    
    # Check backend
    if hasattr(app.embeddings, 'backend'):
        logger.info(f"Backend type: {type(app.embeddings.backend).__name__}")
    else:
        logger.info("Backend: Not initialized")
    
    # Check database
    if hasattr(app.embeddings, 'database'):
        logger.info(f"Database type: {type(app.embeddings.database).__name__ if app.embeddings.database else 'None'}")
        if app.embeddings.database:
            logger.info(f"Database count: {app.embeddings.count() if hasattr(app.embeddings, 'count') else 'Unknown'}")
    else:
        logger.info("Database: Not initialized")
    
    # Check storage path
    if hasattr(app.embeddings, 'config') and 'path' in app.embeddings.config:
        storage_path = app.embeddings.config['path']
        logger.info(f"Storage path: {storage_path}")
        
        # Check if path exists
        if os.path.exists(storage_path):
            logger.info(f"Storage path exists: Yes")
            # List files in storage path
            files = list(Path(storage_path).glob("*"))
            logger.info(f"Files in storage path: {[f.name for f in files]}")
        else:
            logger.info(f"Storage path exists: No")
    else:
        logger.info("Storage path: Not configured")
    
    # Check graph
    if hasattr(app.embeddings, 'graph'):
        logger.info(f"Graph initialized: {app.embeddings.graph is not None}")
        if app.embeddings.graph:
            logger.info(f"Graph type: {type(app.embeddings.graph).__name__}")
            # Try to get graph stats
            try:
                if hasattr(app.embeddings.graph, 'graph'):
                    g = app.embeddings.graph.graph
                    logger.info(f"Graph nodes: {len(g.nodes)}")
                    logger.info(f"Graph edges: {len(g.edges)}")
            except Exception as e:
                logger.error(f"Error getting graph stats: {e}")
    else:
        logger.info("Graph: Not configured")