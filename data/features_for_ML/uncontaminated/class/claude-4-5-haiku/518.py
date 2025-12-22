from datetime import datetime, timedelta
from typing import Any, Dict
import uuid


class Transaction:
    """Represents a database transaction."""
    
    def __init__(self, transaction_id: str, session_id: str, connection: Any):
        self.transaction_id = transaction_id
        self.session_id = session_id
        self.connection = connection
        self.created_at = datetime.now()
        self.status = "active"
    
    def is_abandoned(self, timeout_minutes: int) -> bool:
        elapsed = datetime.now() - self.created_at
        return elapsed > timedelta(minutes=timeout_minutes)


class TransactionManager:
    """Manages database transactions."""

    def __init__(self):
        self._transactions: Dict[str, Transaction] = {}
        self._session_transactions: Dict[str, list] = {}

    def begin_transaction(self, session_id: str, connection: Any) -> str:
        """
        Begin a new transaction for a session.
        
        Args:
            session_id: The session identifier
            connection: The database connection object
            
        Returns:
            The transaction ID
        """
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(transaction_id, session_id, connection)
        
        self._transactions[transaction_id] = transaction
        
        if session_id not in self._session_transactions:
            self._session_transactions[session_id] = []
        self._session_transactions[session_id].append(transaction_id)
        
        return transaction_id

    def get_transaction(self, transaction_id: str) -> Transaction | None:
        """
        Retrieve a transaction by ID.
        
        Args:
            transaction_id: The transaction identifier
            
        Returns:
            The Transaction object or None if not found
        """
        return self._transactions.get(transaction_id)

    def end_transaction(self, transaction_id: str, action: int) -> bool:
        """
        End a transaction with the specified action.
        
        Args:
            transaction_id: The transaction identifier
            action: The action to perform (0=rollback, 1=commit)
            
        Returns:
            True if transaction was successfully ended, False otherwise
        """
        transaction = self._transactions.get(transaction_id)
        
        if transaction is None:
            return False
        
        if transaction.status != "active":
            return False
        
        try:
            if action == 0:  # rollback
                if hasattr(transaction.connection, 'rollback'):
                    transaction.connection.rollback()
            elif action == 1:  # commit
                if hasattr(transaction.connection, 'commit'):
                    transaction.connection.commit()
            else:
                return False
            
            transaction.status = "completed"
            
            # Remove from session transactions
            if transaction.session_id in self._session_transactions:
                if transaction_id in self._session_transactions[transaction.session_id]:
                    self._session_transactions[transaction.session_id].remove(transaction_id)
            
            # Remove from transactions
            del self._transactions[transaction_id]
            
            return True
        except Exception:
            return False

    def cleanup_abandoned_transactions(self, timeout_minutes: int = 30):
        """
        Clean up abandoned transactions that have exceeded the timeout.
        
        Args:
            timeout_minutes: The timeout period in minutes (default: 30)
        """
        abandoned_transaction_ids = []
        
        for transaction_id, transaction in self._transactions.items():
            if transaction.is_abandoned(timeout_minutes):
                abandoned_transaction_ids.append(transaction_id)
        
        for transaction_id in abandoned_transaction_ids:
            transaction = self._transactions[transaction_id]
            
            try:
                if hasattr(transaction.connection, 'rollback'):
                    transaction.connection.rollback()
            except Exception:
                pass
            
            transaction.status = "abandoned"
            
            # Remove from session transactions
            if transaction.session_id in self._session_transactions:
                if transaction_id in self._session_transactions[transaction.session_id]:
                    self._session_transactions[transaction.session_id].remove(transaction_id)
            
            # Remove from transactions
            del self._transactions[transaction_id]