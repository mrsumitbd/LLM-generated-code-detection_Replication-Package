def collection_exists(col):
    """Check if a collection exists in the database."""
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError
    
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        db = client.get_database()
        return col in db.list_collection_names()
    except (ServerSelectionTimeoutError, Exception):
        return False