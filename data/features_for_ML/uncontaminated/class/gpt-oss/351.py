import time
import datetime
from typing import Optional


class QuestionMaker:
    """
    A simple helper class that stores a chat identifier and an optional context string.
    It can return the context prefixed with a timestamp.
    """

    def __init__(self, chat_id: str, context: str = "") -> None:
        """
        Initialize the QuestionMaker with a chat ID and optional context.

        :param chat_id: Identifier for the chat session.
        :param context: Optional initial context string.
        """
        self.chat_id: str = chat_id
        self.context: str = context

    def get_context(self, timestamp: Optional[float] = None) -> str:
        """
        Return the stored context string prefixed with a formatted timestamp.

        :param timestamp: Unix timestamp to use. If None, the current time is used.
        :return: A string containing the timestamp and the context.
        """
        if timestamp is None:
            timestamp = time.time()
        ts_str = datetime.datetime.fromtimestamp(timestamp).isoformat()
        return f"{ts_str} - {self.context}"