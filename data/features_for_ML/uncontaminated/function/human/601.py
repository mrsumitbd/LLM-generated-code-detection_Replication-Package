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