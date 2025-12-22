def _render() -> str:
        parts: list[str] = []
        if header:
            parts.append(header.rstrip())
        parts.append("\n".join(handler._buf))
        if footer:
            parts.append(footer.rstrip())
        return "\n".join(parts)