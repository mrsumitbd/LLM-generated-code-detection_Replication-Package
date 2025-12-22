class ScratchGlobalToggle:

    def __init__(self) -> None:
        self.sockets = {}
        self.nodes = {}

    def create_sockets(self) -> None:
        self.sockets = {
            'input': [],
            'output': []
        }

    def create_nodes(self) -> None:
        self.nodes = {
            'toggle': None,
            'state': False
        }