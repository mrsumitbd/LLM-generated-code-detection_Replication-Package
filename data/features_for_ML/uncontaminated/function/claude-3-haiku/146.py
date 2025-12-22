def assert_same_address(model_ctrl_table, motor_models, data_name):
    """
    Asserts that the addresses in the model_ctrl_table match the addresses in the motor_models for the given data_name.

    Args:
        model_ctrl_table (dict): A dictionary containing the model control table.
        motor_models (list): A list of motor models.
        data_name (str): The name of the data to be checked.

    Raises:
        AssertionError: If the addresses in the model_ctrl_table do not match the addresses in the motor_models for the given data_name.
    """
    for motor_model in motor_models:
        assert motor_model.address == model_ctrl_table[data_name][motor_model.id]['address'], \
            f"Address mismatch for motor model {motor_model.id} and data {data_name}"