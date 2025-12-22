class Resource:
    _id_counter = 0

    def __init__(self, name: str):
        self.name = name
        self.id = Resource._id_counter
        Resource._id_counter += 1
        self._acquired = False

    def acquire(self):
        if self._acquired:
            raise RuntimeError(f"Resource {self.name} already acquired")
        self._acquired = True

    def release(self):
        if not self._acquired:
            raise RuntimeError(f"Resource {self.name} not acquired")
        self._acquired = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False

    def __repr__(self):
        status = "acquired" if self._acquired else "released"
        return f"<Resource id={self.id} name={self.name!r} status={status}>"

    def __str__(self):
        return f"Resource {self.name} (id={self.id})"

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)