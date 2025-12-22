class ActionsResourceWithStreamingResponse:

    def __init__(self, actions: ActionsResource) -> None:
        self._actions = actions

    def __getattr__(self, name: str):
        original_method = getattr(self._actions, name)
        
        if callable(original_method):
            def wrapper(*args, **kwargs):
                kwargs['stream'] = True
                return original_method(*args, **kwargs)
            return wrapper
        
        return original_method