class ScratchGlobalToggle:

    def __init__(self) -> None:
        self.sockets = []
        self.nodes = []

    def create_sockets(self) -> None:
        self.sockets = ['Socket1', 'Socket2', 'Socket3']

    def create_nodes(self) -> None:
        self.nodes = ['Node1', 'Node2', 'Node3']

# Usage example
toggle = ScratchGlobalToggle()
toggle.create_sockets()
toggle.create_nodes()

print(toggle.sockets)
print(toggle.nodes)