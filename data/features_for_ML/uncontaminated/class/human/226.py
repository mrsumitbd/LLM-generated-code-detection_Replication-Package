from typing import TYPE_CHECKING, Any, Callable, List, Optional
import warnings
import omegaconf
from cosmos_transfer1.utils import distributed, log
from cosmos_transfer1.utils.config import Config
from cosmos_transfer1.utils.lazy_config import instantiate
from cosmos_transfer1.utils.trainer import Trainer

class CallBackGroup:
    """A class for hosting a collection of callback objects.

    It is used to execute callback functions of multiple callback objects with the same method name.
    When callbackgroup.func(args) is executed, internally it loops through the objects in self._callbacks and runs
    self._callbacks[0].func(args), self._callbacks[1].func(args), etc. The method name and arguments should match.

    Attributes:
        _callbacks (list[Callback]): List of callback objects.
    """

    def __init__(self, config: Config, trainer: Trainer) -> None:
        """Initializes the list of callback objects.

        Args:
            config (Config): The config object for the codebase.
            trainer (Trainer): The main trainer.
        """
        self._callbacks = []
        callback_configs = config.trainer.callbacks
        if callback_configs:
            if isinstance(callback_configs, list) or isinstance(callback_configs, omegaconf.listconfig.ListConfig):
                warnings.warn(
                    "The 'config.trainer.callbacks' parameter should be a dict instead of a list. "
                    "Please update your code",
                    DeprecationWarning,
                    stacklevel=2,
                )
                callback_configs = {f"callback_{i}": v for i, v in enumerate(callback_configs)}
            for callback_name, current_callback_cfg in callback_configs.items():
                if "_target_" not in current_callback_cfg:
                    log.critical(
                        f"Callback {callback_name} is missing the '_target_' field. \n SKip {current_callback_cfg}"
                    )
                    continue
                log.critical(f"Instantiating callback {callback_name}: {current_callback_cfg}")
                _callback = instantiate(current_callback_cfg)
                assert isinstance(_callback, Callback), f"{current_callback_cfg} is not a valid callback."
                _callback.config = config
                _callback.trainer = trainer
                self._callbacks.append(_callback)

    def __getattr__(self, method_name: str) -> Callable:
        """Loops through the callback objects to call the corresponding callback function.

        Args:
            method_name (str): Callback method name.
        """

        def multi_callback_wrapper(*args, **kwargs) -> None:
            for callback in self._callbacks:
                assert hasattr(callback, method_name)
                method = getattr(callback, method_name)
                assert callable(method)
                _ = method(*args, **kwargs)

        return multi_callback_wrapper