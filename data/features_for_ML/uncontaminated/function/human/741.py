from omegaconf import DictConfig, ListConfig, OmegaConf

def is_serializable(item):
            try:
                OmegaConf.to_yaml(item)
                return True
            except Exception as e:
                return False