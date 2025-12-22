from abc import ABC, abstractmethod

class TransformerBase:
    """Transformer base class."""

    @abstractmethod
    def truncate(self):
        """Truncate operation."""

    @abstractmethod
    def drop(self):
        """Clean operation."""