class AzureOpenAIAPIVersion:
    """Container for Azure OpenAI API version configuration.

    Attributes:
        value (str): The API version for Azure OpenAI services.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, AzureOpenAIAPIVersion):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)