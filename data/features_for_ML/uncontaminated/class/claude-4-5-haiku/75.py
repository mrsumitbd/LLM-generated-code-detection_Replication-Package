class ActionLinker:
    def __init__(self, action):
        self.action = action
    
    def __rshift__(self, other: 'AnyNode[M]') -> 'AnyNode[M]':
        if hasattr(other, 'add_predecessor'):
            other.add_predecessor(self.action)
        return other