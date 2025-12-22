def assert_same_address(model_ctrl_table, motor_models, data_name):
    all_addr = []
    all_bytes = []
    for model in motor_models:
        addr, bytes = model_ctrl_table[model][data_name]
        all_addr.append(addr)
        all_bytes.append(bytes)

    if len(set(all_addr)) != 1:
        raise NotImplementedError(
            f"At least two motor models use a different address for `data_name`='{data_name}' ({list(zip(motor_models, all_addr, strict=False))}). Contact a LeRobot maintainer."
        )

    if len(set(all_bytes)) != 1:
        raise NotImplementedError(
            f"At least two motor models use a different bytes representation for `data_name`='{data_name}' ({list(zip(motor_models, all_bytes, strict=False))}). Contact a LeRobot maintainer."
        )