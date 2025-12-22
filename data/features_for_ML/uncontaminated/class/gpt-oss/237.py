import re
from datetime import datetime
from typing import Optional


class FormatConverter:
    """Convert between different Discord message formats."""

    @staticmethod
    def markdown_to_discord(markdown_text: str) -> str:
        """
        Convert a subset of Markdown syntax to Discord-compatible syntax.
        Discord supports most Markdown natively, but this method also
        converts Markdown links and images to Discord's link syntax.
        """
        if not markdown_text:
            return ""

        # Convert Markdown links [text](url) to Discord <url|text>
        def _link_repl(match: re.Match) -> str:
            text, url = match.group(1), match.group(2)
            return f"<{url}|{text}>"

        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, markdown_text)

        # Convert Markdown images ![alt](url) to Discord <url>
        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"<\2>", text)

        # Escape any remaining backticks that might interfere with code blocks
        text = text.replace("`", r"\`")

        return text

    @staticmethod
    def escape_discord_formatting(text: str) -> str:
        """
        Escape Discord formatting characters by prefixing them with a backslash.
        """
        if not text:
            return ""

        # Characters that need escaping in Discord
        escape_chars = r"&<>\*_\~|`\\"
        # Use regex to escape each character
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """
        Wrap the given code in a Discord code block with an optional language.
        """
        lang = language.strip()
        return f"```{lang}\n{code}\n```"

    @staticmethod
    def format_mention(mention_type: str, id_value: Optional[str] = None) -> str:
        """
        Return a Discord mention string for the given type and ID.
        Supported types: user, role, channel, everyone, here.
        """
        mt = mention_type.lower()
        if mt == "user":
            return f"<@{id_value}>"
        if mt == "role":
            return f"<@&{id_value}>"
        if mt == "channel":
            return f"<#{id_value}>"
        if mt == "everyone":
            return "@everyone"
        if mt == "here":
            return "@here"
        raise ValueError(f"Unsupported mention type: {mention_type}")

    @staticmethod
    def format_timestamp(timestamp: datetime, style: str = "f") -> str:
        """
        Format a datetime object into a Discord timestamp.
        Discord uses the syntax <t:unix_timestamp:style>.
        """
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime instance")
        unix_ts = int(timestamp.timestamp())
        return f"<t:{unix_ts}:{style}>"