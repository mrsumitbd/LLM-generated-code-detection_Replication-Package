import time
from typing import Any, Dict, Optional

class Transaction:
    def __init__(self, transaction_id: str, session_id: str, connection: Any):
        self.transaction_id = transaction_id
        self.session_id = session_id
        self.connection = connection
        self.start_time = time.time()

class TransactionManager:
    """Manages database transactions."""

    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}

    def begin_transaction(self, session_id: str, connection: Any) -> str:
        transaction_id = f"{session_id}_{len(self.transactions) + 1}"
        transaction = Transaction(transaction_id, session_id, connection)
        self.transactions[transaction_id] = transaction
        return transaction_id

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        return self.transactions.get(transaction_id)

    def end_transaction(self, transaction_id: str, action: int) -> bool:
        transaction = self.get_transaction(transaction_id)
        if transaction:
            if action == 0:
                transaction.connection.rollback()
            else:
                transaction.connection.commit()
            del self.transactions[transaction_id]
            return True
        return False

    def cleanup_abandoned_transactions(self, timeout_minutes: int = 30):
        current_time = time.time()
        for transaction_id, transaction in list(self.transactions.items()):
            if current_time - transaction.start_time > timeout_minutes * 60:
                transaction.connection.rollback()
                del self.transactions[transaction_id]