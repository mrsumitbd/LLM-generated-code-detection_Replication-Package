def collection_exists(col):
    from pymongo import MongoClient
    client = MongoClient()
    db = client['your_database_name']
    if col in db.list_collection_names():
        return True
    else:
        return False