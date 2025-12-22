
class ActionLinker:
            def __rshift__(self, other: AnyNode[M]) -> AnyNode[M]:
                """Implement - "action" >> node_b syntax"""
                return that.on(action, other)