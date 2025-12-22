import os
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class _LogRule:
    """A single log rule with pattern and level."""
    pattern: str
    level: str
    compiled_pattern: Optional[re.Pattern] = None
    
    def __post_init__(self):
        try:
            self.compiled_pattern = re.compile(self.pattern)
        except re.error:
            self.compiled_pattern = None


class _LogConfig:
    """Parsed configuration from PYTHON_LOG: default level and per-pattern rules."""
    
    def __init__(self, config_string: Optional[str] = None):
        """Initialize log configuration from PYTHON_LOG environment variable or provided string.
        
        Args:
            config_string: Configuration string in format "DEFAULT_LEVEL;pattern1:level1;pattern2:level2;..."
                          If None, reads from PYTHON_LOG environment variable.
        """
        self.default_level = "WARNING"
        self.rules: list[_LogRule] = []
        
        if config_string is None:
            config_string = os.environ.get("PYTHON_LOG", "")
        
        if config_string:
            self._parse_config(config_string)
    
    def _parse_config(self, config_string: str) -> None:
        """Parse the configuration string.
        
        Format: "DEFAULT_LEVEL;pattern1:level1;pattern2:level2;..."
        """
        parts = config_string.split(";")
        
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            
            if i == 0:
                # First part is the default level
                self.default_level = part.upper()
            else:
                # Subsequent parts are pattern:level rules
                if ":" in part:
                    pattern, level = part.rsplit(":", 1)
                    pattern = pattern.strip()
                    level = level.strip().upper()
                    if pattern and level:
                        self.rules.append(_LogRule(pattern, level))
    
    def get_level_for_name(self, logger_name: str) -> str:
        """Get the log level for a given logger name.
        
        Args:
            logger_name: The name of the logger.
            
        Returns:
            The log level to use for this logger.
        """
        for rule in self.rules:
            if rule.compiled_pattern and rule.compiled_pattern.search(logger_name):
                return rule.level
        
        return self.default_level