class AzureOpenAIAPIVersion:
    """Container for Azure OpenAI API version configuration.

    Attributes:
        value (str): The API version for Azure OpenAI services.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Azure OpenAI API Version: {self.value}"

# Example Usage
api_version = AzureOpenAIAPIVersion("2021-10-01")
print(api_version)