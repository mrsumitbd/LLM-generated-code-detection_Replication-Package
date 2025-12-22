class SCDynamicInputConfiguration:
    """Define defaults for dynamic configuration."""

    def __init__(self) -> None:
        self.input_type = 'text'
        self.placeholder = ''
        self.required = False
        self.min_length = None
        self.max_length = None
        self.pattern = None
        self.options = []
        self.default = None