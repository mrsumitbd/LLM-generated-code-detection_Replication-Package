
class RepeatableIterator:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for phrases in self.data:
            for sentence in phrases:
                yield sentence