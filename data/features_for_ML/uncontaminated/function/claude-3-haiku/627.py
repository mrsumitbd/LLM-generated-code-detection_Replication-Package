import pymongo

def collection_exists(col):
    client = pymongo.MongoClient()
    db = client.get_database()
    return col in db.list_collection_names()