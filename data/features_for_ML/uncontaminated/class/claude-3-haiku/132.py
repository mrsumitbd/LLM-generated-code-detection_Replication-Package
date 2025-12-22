class KeysResourceWithStreamingResponse:
    def __init__(self, keys: KeysResource) -> None:
        self.keys = keys

    def get_keys(self) -> Generator[Key, None, None]:
        for key in self.keys.get_keys():
            yield key

    def get_keys_as_list(self) -> List[Key]:
        return list(self.get_keys())

    def get_keys_as_json(self) -> str:
        keys = self.get_keys_as_list()
        return json.dumps([key.to_dict() for key in keys])