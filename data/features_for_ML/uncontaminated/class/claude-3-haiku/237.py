import datetime

class FormatConverter:
    """Convert between different Discord message formats."""

    @staticmethod
    def markdown_to_discord(markdown_text: str) -> str:
        """Convert Markdown text to Discord formatting."""
        discord_text = markdown_text.replace("*", "\\*")
        discord_text = discord_text.replace("_", "\\_")
        discord_text = discord_text.replace("~", "\\~")
        discord_text = discord_text.replace("`", "\\`")
        discord_text = discord_text.replace("|", "\\|")
        return discord_text

    @staticmethod
    def escape_discord_formatting(text: str) -> str:
        """Escape Discord formatting characters in the given text."""
        return FormatConverter.markdown_to_discord(text)

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """Format the given code as a Discord code block."""
        if language:
            return f"```{language}\n{code}\n```"
        else:
            return f"```\n{code}\n```"

    @staticmethod
    def format_mention(mention_type: str, id_value: str) -> str:
        """Format a mention for the given type and ID."""
        if mention_type == "user":
            return f"<@{id_value}>"
        elif mention_type == "channel":
            return f"<#{id_value}>"
        elif mention_type == "role":
            return f"<@&{id_value}>"
        else:
            return ""

    @staticmethod
    def format_timestamp(timestamp: datetime, style: str = "f") -> str:
        """Format the given timestamp in the specified Discord style."""
        styles = {
            "d": "%m/%d/%Y",
            "D": "%A, %B %d, %Y",
            "f": "%A, %B %d, %Y %I:%M %p",
            "F": "%Y-%m-%d %H:%M:%S",
            "R": "%I:%M %p"
        }
        if style in styles:
            return f"<t:{int(timestamp.timestamp())}:{style}>"
        else:
            return f"<t:{int(timestamp.timestamp())}>"