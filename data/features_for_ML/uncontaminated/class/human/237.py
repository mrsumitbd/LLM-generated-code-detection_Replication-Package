import re
from datetime import datetime

class FormatConverter:
    """Convert between different Discord message formats."""

    @staticmethod
    def markdown_to_discord(markdown_text: str) -> str:
        """
        Convert basic markdown to Discord formatting.

        Args:
            markdown_text: Text with markdown formatting

        Returns:
            Text with Discord formatting
        """
        # Discord uses similar markdown, but with some differences
        conversions = [
            (r"\*\*(.*?)\*\*", r"**\1**"),  # Bold (same)
            (r"\*(.*?)\*", r"*\1*"),  # Italic (same)
            (r"`(.*?)`", r"`\1`"),  # Code (same)
            (r"~~(.*?)~~", r"~~\1~~"),  # Strikethrough (same)
            (r"__(.*?)__", r"__\1__"),  # Underline (same)
        ]

        result = markdown_text
        for pattern, replacement in conversions:
            result = re.sub(pattern, replacement, result)

        return result

    @staticmethod
    def escape_discord_formatting(text: str) -> str:
        """
        Escape Discord formatting characters.

        Args:
            text: Text to escape

        Returns:
            Text with escaped formatting
        """
        escape_chars = ["*", "_", "~", "`", "|", "\\"]

        for char in escape_chars:
            text = text.replace(char, f"\\{char}")

        return text

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """
        Format text as Discord code block.

        Args:
            code: Code content
            language: Programming language for syntax highlighting

        Returns:
            Formatted code block
        """
        return f"```{language}\n{code}\n```"

    @staticmethod
    def format_mention(mention_type: str, id_value: str) -> str:
        """
        Format Discord mentions.

        Args:
            mention_type: Type of mention (user, channel, role)
            id_value: ID to mention

        Returns:
            Formatted mention string
        """
        mention_formats = {
            "user": f"<@{id_value}>",
            "channel": f"<#{id_value}>",
            "role": f"<@&{id_value}>",
        }

        return mention_formats.get(mention_type, f"@{id_value}")

    @staticmethod
    def format_timestamp(timestamp: datetime, style: str = "f") -> str:
        """
        Format timestamp for Discord display.

        Args:
            timestamp: Datetime to format
            style: Discord timestamp style (t, T, d, D, f, F, R)

        Returns:
            Formatted timestamp string
        """
        unix_timestamp = int(timestamp.timestamp())
        return f"<t:{unix_timestamp}:{style}>"