class SCDynamicInputConfiguration:
    """Define defaults for dynamic configuration."""

    def __init__(self) -> None:
        self.enabled = False
        self.update_interval = 60
        self.max_retries = 3
        self.timeout = 30
        self.cache_enabled = True
        self.cache_ttl = 300
        self.validation_enabled = True
        self.error_handling = "strict"
        self.logging_enabled = False
        self.debug_mode = False