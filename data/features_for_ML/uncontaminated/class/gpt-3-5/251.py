class ToolContext:
    """Context passed to tool handlers"""

    def __init__(self, account_manager: AccountManager, messages_func):
        self.account_manager = account_manager
        self.messages_func = messages_func

# Assuming AccountManager class is already defined.