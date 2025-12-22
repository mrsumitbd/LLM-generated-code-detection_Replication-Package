from collections import OrderedDict
from typing import Any, Optional


class MessageCache:
    """
    A simple LRU cache for Message objects keyed by their `id` attribute.
    """

    def __init__(self, max_size: int = 10000):
        """
        Create a new MessageCache.

        Parameters
        ----------
        max_size : int, optional
            The maximum number of messages to keep in the cache. When the
            limit is exceeded, the oldest entry is discarded. Defaults to 10_000.
        """
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()

    def get_message(self, id: str) -> Optional[Any]:
        """
        Retrieve a message from the cache by its id.

        Parameters
        ----------
        id : str
            The identifier of the message to retrieve.

        Returns
        -------
        Optional[Message]
            The cached message if present, otherwise None.
        """
        return self._cache.get(id)

    def add_message(self, message: Any) -> None:
        """
        Add a message to the cache.

        Parameters
        ----------
        message : Message
            The message object to cache. It must expose an `id` attribute
            that is a string.

        Raises
        ------
        ValueError
            If the message does not have an `id` attribute.
        """
        # Extract the id from the message.  We use getattr to avoid
        # AttributeError if the attribute is missing.
        msg_id = getattr(message, "id", None)
        if msg_id is None:
            raise ValueError("Message object must have an 'id' attribute")

        # If the message is already cached, move it to the end to mark it
        # as most recently used.
        if msg_id in self._cache:
            self._cache.move_to_end(msg_id)
            return

        # Evict the oldest entry if we are at capacity.
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)

        # Insert the new message.
        self._cache[msg_id] = message