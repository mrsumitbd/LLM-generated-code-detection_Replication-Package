class KeysResourceWithStreamingResponse:
    
    def __init__(self, keys: KeysResource) -> None:
        self.keys = keys

    def get_keys(self):
        return self.keys.get_keys()

    def stream_keys(self):
        for key in self.keys.get_keys():
            yield key