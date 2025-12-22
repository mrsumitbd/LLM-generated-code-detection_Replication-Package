def load_patch_model_from_single_file(state_dict, model_names, model_classes, extra_kwargs, model_manager, torch_dtype, device):
    models = {}
    for model_name, model_class in zip(model_names, model_classes):
        model = model_class(**extra_kwargs)
        model.load_state_dict(state_dict[model_name])
        model.to(torch_dtype).to(device)
        models[model_name] = model
    model_manager.add_models(models)