class CallBackGroup:
    """A class for hosting a collection of callback objects.

    It is used to execute callback functions of multiple callback objects with the same method name.
    When callbackgroup.func(args) is executed, internally it loops through the objects in self._callbacks and runs
    self._callbacks[0].func(args), self._callbacks[1].func(args), etc. The method name and arguments should match.

    Attributes:
        _callbacks (list[Callback]): List of callback objects.
    """

    def __init__(self, config: Config, trainer: Trainer) -> None:
        self._callbacks = []
        self._add_callbacks(config, trainer)

    def __getattr__(self, method_name: str) -> Callable:
        def wrapper(*args, **kwargs):
            for callback in self._callbacks:
                getattr(callback, method_name)(*args, **kwargs)
        return wrapper

    def _add_callbacks(self, config: Config, trainer: Trainer) -> None:
        for callback_class in config.callbacks:
            self._callbacks.append(callback_class(config, trainer))