from datetime import datetime
import re

class FormatConverter:
    """Convert between different Discord message formats."""

    @staticmethod
    def markdown_to_discord(markdown_text: str) -> str:
        """Convert markdown formatting to Discord formatting."""
        # Convert **bold** to **bold**
        markdown_text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', markdown_text)
        # Convert __underline__ to __underline__
        markdown_text = re.sub(r'__(.*?)__', r'__\1__', markdown_text)
        # Convert *italic* to *italic*
        markdown_text = re.sub(r'\*(.*?)\*', r'*\1*', markdown_text)
        # Convert _italic_ to _italic_
        markdown_text = re.sub(r'_(.*?)_', r'_\1_', markdown_text)
        # Convert ~~strikethrough~~ to ~~strikethrough~~
        markdown_text = re.sub(r'~~(.*?)~~', r'~~\1~~', markdown_text)
        # Convert `code` to `code`
        markdown_text = re.sub(r'`(.*?)`', r'`\1`', markdown_text)
        return markdown_text

    @staticmethod
    def escape_discord_formatting(text: str) -> str:
        """Escape Discord formatting characters."""
        # Escape backslashes first
        text = text.replace('\\', '\\\\')
        # Escape asterisks
        text = text.replace('*', '\\*')
        # Escape underscores
        text = text.replace('_', '\\_')
        # Escape backticks
        text = text.replace('`', '\\`')
        # Escape tildes
        text = text.replace('~', '\\~')
        # Escape pipes
        text = text.replace('|', '\\|')
        # Escape greater than
        text = text.replace('>', '\\>')
        return text

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """Format code as a Discord code block."""
        return f"```{language}\n{code}\n```"

    @staticmethod
    def format_mention(mention_type: str, id_value: str) -> str:
        """Format a mention for Discord."""
        mention_type = mention_type.lower()
        
        if mention_type == "user":
            return f"<@{id_value}>"
        elif mention_type == "role":
            return f"<@&{id_value}>"
        elif mention_type == "channel":
            return f"<#{id_value}>"
        elif mention_type == "emoji":
            return f"<:{id_value}>"
        else:
            return f"<@{id_value}>"

    @staticmethod
    def format_timestamp(timestamp: datetime, style: str = "f") -> str:
        """Format a timestamp for Discord."""
        # Discord timestamp format: <t:unix_timestamp:style>
        unix_timestamp = int(timestamp.timestamp())
        
        # Valid styles: t (short time), T (long time), d (short date), D (long date),
        # f (short date/time), F (long date/time), R (relative)
        valid_styles = ['t', 'T', 'd', 'D', 'f', 'F', 'R']
        
        if style not in valid_styles:
            style = 'f'
        
        return f"<t:{unix_timestamp}:{style}>"