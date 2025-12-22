def assert_same_address(model_ctrl_table, motor_models, data_name):
    """
    Assert that all motor models have the same address for a given data name.
    
    Args:
        model_ctrl_table: Dictionary mapping model names to control tables
        motor_models: List of motor model names to check
        data_name: Name of the data field to check addresses for
    
    Raises:
        AssertionError: If not all models have the same address for the data_name
    """
    if not motor_models:
        return
    
    addresses = []
    for model in motor_models:
        if model in model_ctrl_table:
            ctrl_table = model_ctrl_table[model]
            if data_name in ctrl_table:
                address = ctrl_table[data_name].get('address')
                addresses.append(address)
    
    if addresses:
        first_address = addresses[0]
        assert all(addr == first_address for addr in addresses), \
            f"Not all motor models have the same address for '{data_name}'. Addresses: {set(addresses)}"