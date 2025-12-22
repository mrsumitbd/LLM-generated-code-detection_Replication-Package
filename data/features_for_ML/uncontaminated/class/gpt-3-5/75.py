from typing import TypeVar

M = TypeVar('M')

class AnyNode:
    def __init__(self, value: M):
        self.value = value

class ActionLinker:
    def __rshift__(self, other: AnyNode[M]) -> AnyNode[M]:
        pass