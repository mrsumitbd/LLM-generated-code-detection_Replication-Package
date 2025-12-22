def escape_discord_formatting(text: str) -> str:
    escaped_text = text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('~', '\\~').replace('|', '\\|')
    return escaped_text