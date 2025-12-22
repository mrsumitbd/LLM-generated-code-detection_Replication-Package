class ToolContext:
    """Context passed to tool handlers"""

    def __init__(self, account_manager: AccountManager, messages_func):
        self._account_manager = account_manager
        self._messages_func = messages_func

    @property
    def account_manager(self) -> AccountManager:
        return self._account_manager

    @property
    def messages(self):
        return self._messages_func()