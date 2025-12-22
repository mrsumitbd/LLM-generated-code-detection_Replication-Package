import torch
from collections import defaultdict

def load_patch_model_from_single_file(
    state_dict,
    model_names,
    model_classes,
    extra_kwargs,
    model_manager,
    torch_dtype,
    device,
):
    """
    Load one or more sub‑models from a single state_dict.

    Parameters
    ----------
    state_dict : dict
        The full state dictionary that may contain parameters for several
        sub‑models. Keys are expected to be prefixed with the model name
        followed by a dot (e.g. "model_a.weight").
    model_names : list[str]
        Names of the sub‑models to instantiate and load.
    model_classes : dict[str, type]
        Mapping from model name to the class that should be instantiated.
    extra_kwargs : dict[str, dict]
        Optional keyword arguments for each model constructor.
    model_manager : object or None
        An optional manager that will receive the loaded models.  If it has a
        ``register(name, model)`` method it will be used; otherwise the
        manager is ignored.
    torch_dtype : torch.dtype
        The dtype to cast the model parameters to.
    device : torch.device or str
        The device on which the model should reside.

    Returns
    -------
    dict[str, torch.nn.Module]
        Mapping from model name to the loaded model instance.
    """
    if isinstance(device, str):
        device = torch.device(device)

    loaded_models = {}

    # Helper to register a model with the manager if possible
    def _register(name, model):
        if model_manager is None:
            return
        # Prefer a register method if it exists
        if hasattr(model_manager, "register"):
            try:
                model_manager.register(name, model)
                return
            except Exception:
                pass
        # Fallback: if manager behaves like a dict
        if isinstance(model_manager, dict):
            model_manager[name] = model

    # If only one model and the state_dict keys are not prefixed,
    # we can load the whole dict directly.
    single = len(model_names) == 1
    if single:
        name = model_names[0]
        cls = model_classes[name]
        kwargs = extra_kwargs.get(name, {})
        model = cls(**kwargs)
        try:
            model.load_state_dict(state_dict, strict=False)
        except RuntimeError:
            # Try to load with strict=True if possible
            model.load_state_dict(state_dict, strict=True)
        model.to(device=device, dtype=torch_dtype)
        loaded_models[name] = model
        _register(name, model)
        return loaded_models

    # For multiple models, split the state_dict by prefix
    for name in model_names:
        cls = model_classes[name]
        kwargs = extra_kwargs.get(name, {})
        model = cls(**kwargs)

        # Extract sub‑dict for this model
        prefix = f"{name}."
        sub_dict = {}
        for k, v in state_dict.items():
            if k.startswith(prefix):
                sub_dict[k[len(prefix) :]] = v

        # If no prefixed keys found, try loading the whole dict
        if not sub_dict:
            sub_dict = state_dict

        try:
            model.load_state_dict(sub_dict, strict=False)
        except RuntimeError:
            # Fallback to strict=True if possible
            model.load_state_dict(sub_dict, strict=True)

        model.to(device=device, dtype=torch_dtype)
        loaded_models[name] = model
        _register(name, model)

    return loaded_models