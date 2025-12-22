class CallBackGroup:
    """A class for hosting a collection of callback objects.

    It is used to execute callback functions of multiple callback objects with the same method name.
    When callbackgroup.func(args) is executed, internally it loops through the objects in self._callbacks and runs
    self._callbacks[0].func(args), self._callbacks[1].func(args), etc. The method name and arguments should match.

    Attributes:
        _callbacks (list[Callback]): List of callback objects.
    """

    def __init__(self, config: Config, trainer: Trainer) -> None:
        self._callbacks = [callback_class(config, trainer) for callback_class in config.callbacks]

    def __getattr__(self, method_name: str) -> Callable:
        def callback_method(*args, **kwargs):
            for callback in self._callbacks:
                if hasattr(callback, method_name):
                    method = getattr(callback, method_name)
                    if callable(method):
                        method(*args, **kwargs)
        return callback_method