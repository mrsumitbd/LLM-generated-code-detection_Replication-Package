class AzureOpenAIAPIVersion:
    """Container for Azure OpenAI API version configuration.

    Attributes:
        value (str): The API version for Azure OpenAI services.
    """

    def __init__(self, value: str):
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val: str):
        if not isinstance(val, str):
            raise TypeError("API version must be a string")
        if not val.strip():
            raise ValueError("API version cannot be empty")
        self._value = val

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r})"

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, AzureOpenAIAPIVersion):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)