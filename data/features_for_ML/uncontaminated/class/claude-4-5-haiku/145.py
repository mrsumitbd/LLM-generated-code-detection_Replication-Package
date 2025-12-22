class NumberFormatConfig:
    """Configuration for Count Bits dataset generation"""

    def __init__(self, base: int = 10, min_value: int = 0, max_value: int = 1000, 
                 padding: int = 0, prefix: str = "", suffix: str = ""):
        self.base = base
        self.min_value = min_value
        self.max_value = max_value
        self.padding = padding
        self.prefix = prefix
        self.suffix = suffix

    def validate(self):
        if not isinstance(self.base, int) or self.base < 2 or self.base > 36:
            raise ValueError("base must be an integer between 2 and 36")
        
        if not isinstance(self.min_value, int):
            raise ValueError("min_value must be an integer")
        
        if not isinstance(self.max_value, int):
            raise ValueError("max_value must be an integer")
        
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        
        if not isinstance(self.padding, int) or self.padding < 0:
            raise ValueError("padding must be a non-negative integer")
        
        if not isinstance(self.prefix, str):
            raise ValueError("prefix must be a string")
        
        if not isinstance(self.suffix, str):
            raise ValueError("suffix must be a string")
        
        return True