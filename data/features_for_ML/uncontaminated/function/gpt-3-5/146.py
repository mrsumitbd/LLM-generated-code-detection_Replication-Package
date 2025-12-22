def assert_same_address(model_ctrl_table, motor_models, data_name):
    for model in motor_models:
        if model_ctrl_table[model] != model_ctrl_table[motor_models[0]]:
            raise ValueError(f"Address mismatch for {data_name} in models {model} and {motor_models[0]}")