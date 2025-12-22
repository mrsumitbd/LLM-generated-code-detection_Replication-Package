class AzureOpenAIAPIVersion:
    """Container for Azure OpenAI API version configuration.

    Attributes:
        value (str): The API version for Azure OpenAI services.
    """

    def __init__(self, value: str) -> None:
        """Initialize AzureOpenAIAPIVersion with an API version string.

        Args:
            value (str): The API version for Azure OpenAI services.
        """
        self.value = value

    def __str__(self) -> str:
        """Return string representation of the API version.

        Returns:
            str: The API version value.
        """
        return self.value

    def __repr__(self) -> str:
        """Return detailed string representation of the object.

        Returns:
            str: Detailed representation including class name and value.
        """
        return f"AzureOpenAIAPIVersion(value={self.value!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another object.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if both objects have the same value, False otherwise.
        """
        if isinstance(other, AzureOpenAIAPIVersion):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False

    def __hash__(self) -> int:
        """Return hash of the API version value.

        Returns:
            int: Hash of the value.
        """
        return hash(self.value)