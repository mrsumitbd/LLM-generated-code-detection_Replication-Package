from omegaconf import DictConfig, ListConfig, OmegaConf
from imaginaire.utils import log

def serialize_config(config):
            if isinstance(config, DictConfig):
                for key, value in config.items():
                    if isinstance(value, (DictConfig, ListConfig)):
                        try:
                            if "_target_" in value:
                                default_params = get_default_params(value["_target_"])
                                for default_key, default_v in default_params.items():
                                    if default_key not in value:
                                        value[default_key] = default_v
                        except Exception as e:
                            log.error(f"Failed to add default argument values: {e}")

                        serialize_config(value)
                    else:
                        if not is_serializable(value) and value is not None:
                            config[key] = str(value)
            elif isinstance(config, ListConfig):
                for i, item in enumerate(config):
                    if isinstance(item, (DictConfig, ListConfig)):
                        serialize_config(item)
                    else:
                        if not is_serializable(item) and item is not None:
                            config[i] = str(item)
            else:
                raise NotImplementedError("Input config must be a DictConfig or ListConfig.")
            return config