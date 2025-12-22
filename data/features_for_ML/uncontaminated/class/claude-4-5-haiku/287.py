class ColorCodes:
    """
    Color codes for rich text output
    """
    
    # ANSI color codes
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright/Bold color codes
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background color codes
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text style codes
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Reset code
    RESET = '\033[0m'
    
    @classmethod
    def colorize(cls, text, color):
        """
        Apply a color code to text
        
        Args:
            text: The text to colorize
            color: The color code to apply
            
        Returns:
            The colorized text with reset code at the end
        """
        return f"{color}{text}{cls.RESET}"
    
    @classmethod
    def get_color_by_name(cls, name):
        """
        Get a color code by its name
        
        Args:
            name: The name of the color (e.g., 'RED', 'BLUE')
            
        Returns:
            The color code, or None if not found
        """
        return getattr(cls, name.upper(), None)