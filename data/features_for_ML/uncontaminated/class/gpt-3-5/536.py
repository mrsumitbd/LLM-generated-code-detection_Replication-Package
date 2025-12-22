from abc import ABC, abstractmethod

class TransformerBase(ABC):
    """Transformer base class."""

    @abstractmethod
    def truncate(self):
        pass

    @abstractmethod
    def drop(self):
        pass