from typing import Generic, TypeVar

M = TypeVar('M')

class AnyNode(Generic[M]):
    pass

class ActionLinker:
    def __rshift__(self, other: AnyNode[M]) -> AnyNode[M]:
        # Implement the logic for the right-shift operator
        # This method should take an AnyNode[M] object as input
        # and return an AnyNode[M] object as output
        # The implementation should link the current action with the provided AnyNode[M] object
        
        # Example implementation:
        linked_node = other
        # Perform any necessary operations to link the current action with the provided node
        return linked_node