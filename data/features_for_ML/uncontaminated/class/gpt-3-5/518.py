from typing import Any

class Transaction:
    def __init__(self, session_id: str, connection: Any):
        self.session_id = session_id
        self.connection = connection
        self.transaction_id = None

class TransactionManager:
    """Manages database transactions."""

    def __init__(self):
        self.transactions = {}

    def begin_transaction(self, session_id: str, connection: Any) -> str:
        transaction = Transaction(session_id, connection)
        transaction_id = str(hash(transaction))
        transaction.transaction_id = transaction_id
        self.transactions[transaction_id] = transaction
        return transaction_id

    def get_transaction(self, transaction_id: str) -> Transaction | None:
        return self.transactions.get(transaction_id)

    def end_transaction(self, transaction_id: str, action: int) -> bool:
        transaction = self.transactions.get(transaction_id)
        if transaction:
            del self.transactions[transaction_id]
            return True
        return False

    def cleanup_abandoned_transactions(self, timeout_minutes: int = 30):
        current_time = time.time()
        for transaction_id, transaction in list(self.transactions.items()):
            if current_time - transaction.start_time > timeout_minutes * 60:
                del self.transactions[transaction_id]