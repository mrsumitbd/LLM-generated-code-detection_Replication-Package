from __future__ import annotations

import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# Simple status constants
STATUS_ACTIVE = "active"
STATUS_COMMITTED = "committed"
STATUS_ABORTED = "aborted"


@dataclass
class Transaction:
    """Represents a single database transaction."""
    transaction_id: str
    session_id: str
    connection: Any
    start_time: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    status: str = field(default=STATUS_ACTIVE)


class TransactionManager:
    """Manages database transactions."""

    def __init__(self) -> None:
        # Store transactions by their ID
        self._transactions: Dict[str, Transaction] = {}

    def begin_transaction(self, session_id: str, connection: Any) -> str:
        """
        Start a new transaction for the given session and connection.

        Returns the generated transaction ID.
        """
        transaction_id = str(uuid.uuid4())
        txn = Transaction(
            transaction_id=transaction_id,
            session_id=session_id,
            connection=connection,
        )
        self._transactions[transaction_id] = txn
        return transaction_id

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """
        Retrieve a transaction by its ID.

        Returns None if the transaction does not exist.
        """
        return self._transactions.get(transaction_id)

    def end_transaction(self, transaction_id: str, action: int) -> bool:
        """
        End a transaction.

        Parameters
        ----------
        transaction_id : str
            The ID of the transaction to end.
        action : int
            0 to commit, any other value to abort.

        Returns
        -------
        bool
            True if the transaction was found and ended, False otherwise.
        """
        txn = self._transactions.get(transaction_id)
        if not txn or txn.status != STATUS_ACTIVE:
            return False

        if action == 0:
            txn.status = STATUS_COMMITTED
        else:
            txn.status = STATUS_ABORTED

        # In a real implementation we would close the connection or
        # perform commit/rollback here. For this simplified example
        # we just remove the transaction from the manager.
        del self._transactions[transaction_id]
        return True

    def cleanup_abandoned_transactions(self, timeout_minutes: int = 30) -> None:
        """
        Remove transactions that have been active longer than the timeout.

        Parameters
        ----------
        timeout_minutes : int, optional
            The age threshold in minutes. Defaults to 30.
        """
        now = datetime.datetime.utcnow()
        timeout = datetime.timedelta(minutes=timeout_minutes)
        to_remove = [
            tid
            for tid, txn in self._transactions.items()
            if txn.status == STATUS_ACTIVE and (now - txn.start_time) > timeout
        ]
        for tid in to_remove:
            # In a real system we might log or attempt to abort the transaction.
            del self._transactions[tid]