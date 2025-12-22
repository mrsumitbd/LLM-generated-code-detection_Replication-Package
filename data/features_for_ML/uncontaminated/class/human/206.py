
class BatchAction:
    """Represents a batch action for a NEAR promise."""

    CREATE_ACCOUNT = "create_account"
    DEPLOY_CONTRACT = "deploy_contract"
    FUNCTION_CALL = "function_call"
    TRANSFER = "transfer"
    STAKE = "stake"
    ADD_KEY_FULL_ACCESS = "add_key_full_access"
    ADD_KEY_FUNCTION_CALL = "add_key_function_call"
    DELETE_KEY = "delete_key"
    DELETE_ACCOUNT = "delete_account"