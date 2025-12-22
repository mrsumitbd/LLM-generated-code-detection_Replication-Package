class ScratchGlobalToggle:
    def __init__(self) -> None:
        # Store sockets and nodes in simple containers
        self.sockets: dict[str, dict] = {}
        self.nodes: list[dict] = []

    def create_sockets(self) -> None:
        """
        Create a minimal set of sockets for the toggle.
        """
        # Input socket: a boolean that can be toggled
        self.sockets["input"] = {"type": "bool", "value": False}
        # Output socket: reflects the current state
        self.sockets["output"] = {"type": "bool", "value": False}

    def create_nodes(self) -> None:
        """
        Create a node that connects the input and output sockets.
        """
        node = {
            "name": "GlobalToggleNode",
            "inputs": ["input"],
            "outputs": ["output"],
            "execute": self._toggle_execute,
        }
        self.nodes.append(node)

    # Internal helper to simulate node execution
    def _toggle_execute(self) -> None:
        """
        Toggle the output value based on the input.
        """
        input_val = self.sockets["input"]["value"]
        # Flip the boolean value
        self.sockets["output"]["value"] = not input_val
        # Update the input to the new state for next call
        self.sockets["input"]["value"] = self.sockets["output"]["value"]