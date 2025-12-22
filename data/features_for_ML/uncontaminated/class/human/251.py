from ..services.email_service import EmailService
from ..services import (
            EmailService, 
            CommunicationService, 
            FolderService, 
            SystemService
        )
from ..account_manager import AccountManager

class ToolContext:
    """Context passed to tool handlers"""
    def __init__(self, account_manager: AccountManager, messages_func):
        self.account_manager = account_manager
        self.get_message = messages_func
        # Initialize all services
        from ..services import (
            EmailService, 
            CommunicationService, 
            FolderService, 
            SystemService
        )
        self.email_service = EmailService(account_manager)
        self.communication_service = CommunicationService(account_manager)
        self.folder_service = FolderService(account_manager)
        self.system_service = SystemService(account_manager)