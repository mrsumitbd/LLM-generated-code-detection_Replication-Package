def sanitize_input(text: str) -> str:
    # Remove potentially dangerous characters
    text = text.replace("<script", "&lt;script")
    text = text.replace("</script>", "&lt;/script&gt;")
    text = text.replace("javascript:", "")
    text = text.replace("data:", "")

    # Limit length
    if len(text) > 10000:
        text = text[:10000] + "... [truncated]"

    return text