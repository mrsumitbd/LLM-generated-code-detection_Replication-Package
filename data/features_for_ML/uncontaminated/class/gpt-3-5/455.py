class TransformedFeynmanDataModule:

    def __init__(self):
        self._name = "TransformedFeynmanDataModule"

    def setup(self):
        # Add setup logic here
        pass

    @property
    def name(self):
        return self._name

# Example usage
data_module = TransformedFeynmanDataModule()
data_module.setup()
print(data_module.name)