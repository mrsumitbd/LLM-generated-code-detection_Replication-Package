from abc import ABC, abstractmethod

class TransformerBase(ABC):
    """Transformer base class."""

    @abstractmethod
    def truncate(self):
        """Truncate the transformer."""
        pass

    @abstractmethod
    def drop(self):
        """Drop the transformer."""
        pass