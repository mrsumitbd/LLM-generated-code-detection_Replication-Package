class BaseConfig:
    @staticmethod
    def from_dict(config_class, config_dict):
        """
        Create an instance of `config_class` using the key/value pairs in `config_dict`.

        Parameters
        ----------
        config_class : type
            The class to instantiate. It should accept keyword arguments that match the keys in `config_dict`.
        config_dict : dict
            A dictionary containing configuration values.

        Returns
        -------
        instance of config_class
            The instantiated configuration object.
        """
        if not isinstance(config_dict, dict):
            raise TypeError(f"config_dict must be a dict, got {type(config_dict).__name__}")

        # Filter out any keys that are not accepted by the constructor
        # This allows passing a superset of keys without raising an error.
        try:
            # Attempt to instantiate directly
            return config_class(**config_dict)
        except TypeError as exc:
            # If the constructor complains about unexpected arguments,
            # try to filter them out.
            import inspect
            sig = inspect.signature(config_class.__init__)
            accepted = {
                name
                for name, param in sig.parameters.items()
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
                and name != "self"
            }
            filtered = {k: v for k, v in config_dict.items() if k in accepted}
            try:
                return config_class(**filtered)
            except Exception:
                # Re‑raise the original error for clarity
                raise exc