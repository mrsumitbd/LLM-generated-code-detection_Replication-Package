def collection_exists(col):
    """
    Check whether a MongoDB collection with the given name exists.

    The function attempts to use a globally defined `client` (an instance of
    `pymongo.MongoClient`). If no client is available or an error occurs,
    the function returns False.

    Parameters
    ----------
    col : str
        The name of the collection to check.

    Returns
    -------
    bool
        True if the collection exists, False otherwise.
    """
    try:
        # Try to get a globally defined MongoClient instance
        client = globals().get("client")
        if client is None:
            return False

        # Use the default database if one is set, otherwise raise an error
        db = client.get_default_database()
        if db is None:
            return False

        return col in db.list_collection_names()
    except Exception:
        return False