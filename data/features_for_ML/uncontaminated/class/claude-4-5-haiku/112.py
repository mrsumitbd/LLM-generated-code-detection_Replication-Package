class ResourceStore:

    def __init__(self, *, store: ObjectStore, presigned_url_expiration: timedelta = timedelta(days=7)) -> None:
        self.store = store
        self.presigned_url_expiration = presigned_url_expiration