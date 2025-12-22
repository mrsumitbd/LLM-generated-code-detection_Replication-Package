class RepeatableIterator:
    def __init__(self, data):
        # Store the data as a list to allow repeated iteration
        self._data = list(data)

    def __iter__(self):
        # Return a new iterator over the stored data each time
        return iter(self._data)