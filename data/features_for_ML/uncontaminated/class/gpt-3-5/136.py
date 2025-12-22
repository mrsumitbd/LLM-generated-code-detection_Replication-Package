class ClientCapability:
    """Represents client capabilities."""

    def __init__(self):
        self.capabilities = {}

    def to_dict(self) -> Dict[str, Any]:
        return self.capabilities

    def add_capability(self, key: str, value: Any):
        self.capabilities[key] = value

# Example usage:
client = ClientCapability()
client.add_capability('browser', 'Chrome')
client.add_capability('version', 91)
print(client.to_dict())