from __future__ import annotations
from typing import Any, Generic, TypeVar

M = TypeVar("M")

class AnyNode(Generic[M]):
    """
    A minimal node class used by ActionLinker.
    """
    def __init__(self, value: M) -> None:
        self.value: M = value
        self.prev: AnyNode[M] | None = None
        self.next: AnyNode[M] | None = None

    def __repr__(self) -> str:
        return f"AnyNode({self.value!r})"


class ActionLinker:
    """
    Provides a convenient way to link nodes using the >> operator.
    """
    def __init__(self, node: AnyNode[M]) -> None:
        self.node = node

    def __rshift__(self, other: AnyNode[M]) -> AnyNode[M]:
        """
        Link the current node to `other` and return `other`.

        The linking is bidirectional: the current node's `next` points to
        `other`, and `other`'s `prev` points back to the current node.
        """
        self.node.next = other
        other.prev = self.node
        return other