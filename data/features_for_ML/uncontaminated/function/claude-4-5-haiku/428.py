import torch
import comfy.model_management as mm
from comfy.sd import load_checkpoint_guess_config


def load_patch_model_from_single_file(state_dict, model_names, model_classes, extra_kwargs, model_manager, torch_dtype, device):
    """
    Load a patch model from a single file's state dict.
    
    Args:
        state_dict: The state dictionary containing model weights
        model_names: List of model names to load
        model_classes: List of model classes corresponding to model_names
        extra_kwargs: Extra keyword arguments for model initialization
        model_manager: The model manager instance
        torch_dtype: The torch dtype to use
        device: The device to load the model on
    
    Returns:
        A dictionary mapping model names to loaded models
    """
    loaded_models = {}
    
    for model_name, model_class in zip(model_names, model_classes):
        # Filter state dict for this specific model
        model_state_dict = {}
        prefix = f"{model_name}."
        
        for key, value in state_dict.items():
            if key.startswith(prefix):
                # Remove the prefix from the key
                new_key = key[len(prefix):]
                model_state_dict[new_key] = value
        
        # If no prefixed keys found, try using the entire state dict
        if not model_state_dict:
            model_state_dict = state_dict
        
        # Initialize the model
        kwargs = extra_kwargs.copy() if extra_kwargs else {}
        kwargs['dtype'] = torch_dtype
        kwargs['device'] = device
        
        try:
            model = model_class(**kwargs)
            
            # Load the state dict into the model
            if hasattr(model, 'load_state_dict'):
                model.load_state_dict(model_state_dict, strict=False)
            
            # Move model to device
            if hasattr(model, 'to'):
                model = model.to(device)
            
            loaded_models[model_name] = model
        except Exception as e:
            print(f"Warning: Failed to load model {model_name}: {e}")
            continue
    
    return loaded_models