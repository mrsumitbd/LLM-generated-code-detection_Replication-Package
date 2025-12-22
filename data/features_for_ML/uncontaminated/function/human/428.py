def load_patch_model_from_single_file(state_dict, model_names, model_classes, extra_kwargs, model_manager, torch_dtype, device):
    loaded_model_names, loaded_models = [], []
    for model_name, model_class in zip(model_names, model_classes):
        while True:
            for model_id in range(len(model_manager.model)):
                base_model_name = model_manager.model_name[model_id]
                if base_model_name == model_name:
                    base_model_path = model_manager.model_path[model_id]
                    base_model = model_manager.model[model_id]
                    print(f"    Adding patch model to {base_model_name} ({base_model_path})")
                    patched_model = load_single_patch_model_from_single_file(
                        state_dict, model_name, model_class, base_model, extra_kwargs, torch_dtype, device)
                    loaded_model_names.append(base_model_name)
                    loaded_models.append(patched_model)
                    model_manager.model.pop(model_id)
                    model_manager.model_path.pop(model_id)
                    model_manager.model_name.pop(model_id)
                    break
            else:
                break
    return loaded_model_names, loaded_models