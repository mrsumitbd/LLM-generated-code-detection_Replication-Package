import re

def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """
        Apply consistent spacing around assignment operators.

        Args:
            line: The line to format
            use_spaces: Whether to use spaces around operators

        Returns:
            The formatted line
        """
        patterns = PatternUtils.ASSIGNMENT_PATTERNS[
            "spaced" if use_spaces else "compact"
        ]

        for pattern, replacement in patterns:
            new_line = re.sub(pattern, replacement, line)
            if new_line != line:
                return new_line

        return line