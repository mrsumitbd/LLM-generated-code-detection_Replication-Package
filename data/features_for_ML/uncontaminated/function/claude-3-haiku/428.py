def load_patch_model_from_single_file(state_dict, model_names, model_classes, extra_kwargs, model_manager, torch_dtype, device):
    models = []
    for model_name, model_class in zip(model_names, model_classes):
        model = model_class(**extra_kwargs.get(model_name, {}))
        model.to(device=device, dtype=torch_dtype)
        model.load_state_dict(state_dict[model_name])
        models.append(model)

    model_manager.register_models(models)
    return models