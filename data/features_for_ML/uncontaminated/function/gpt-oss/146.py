def assert_same_address(model_ctrl_table, motor_models, data_name):
    """
    Assert that the address for ``data_name`` in ``motor_models`` matches the
    address in ``model_ctrl_table``.  ``model_ctrl_table`` is expected to be a
    mapping from data names to addresses.  ``motor_models`` can be one of the
    following:

    * a mapping from model identifiers to addresses for the given data name
    * a sequence of addresses
    * an object that exposes the address via an attribute or key lookup

    If any address does not match the expected value an AssertionError is
    raised.
    """
    # Ensure the data name exists in the control table
    if data_name not in model_ctrl_table:
        raise AssertionError(
            f"data_name '{data_name}' not found in model_ctrl_table"
        )

    expected_addr = model_ctrl_table[data_name]

    # Helper to compare a single address
    def _check(addr, identifier):
        if addr != expected_addr:
            raise AssertionError(
                f"Address mismatch for {identifier} on '{data_name}': "
                f"expected {expected_addr}, got {addr}"
            )

    # Case 1: motor_models is a mapping (e.g., dict)
    if isinstance(motor_models, dict):
        for model_id, addr in motor_models.items():
            _check(addr, model_id)

    # Case 2: motor_models is a sequence (list, tuple, set, etc.)
    elif isinstance(motor_models, (list, tuple, set)):
        for idx, addr in enumerate(motor_models):
            _check(addr, f"index {idx}")

    # Case 3: motor_models is a single object that may expose the address
    else:
        # Try attribute access
        try:
            addr = getattr(motor_models, data_name)
        except AttributeError:
            # Try key access
            try:
                addr = motor_models[data_name]
            except Exception:
                raise AssertionError(
                    f"Cannot retrieve address for '{data_name}' from motor_models"
                )
        _check(addr, "motor_models")