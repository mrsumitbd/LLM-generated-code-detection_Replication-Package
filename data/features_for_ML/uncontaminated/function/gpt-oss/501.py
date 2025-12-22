import re

def path_to_regex(path: str) -> str:
    """
    Convert a URL path with parameter syntax into a regular expression string.
    Supported syntax: <converter:name> where converter can be one of:
        int   -> \d+
        str   -> [^/]+
        path  -> .+
        uuid  -> [0-9a-fA-F-]+
        float -> \d+(?:\.\d+)?
    If no converter is specified, 'str' is assumed.
    The returned regex is anchored with ^ and $.
    """
    # Mapping of converters to regex patterns
    converter_map = {
        "int": r"\d+",
        "str": r"[^/]+",
        "path": r".+",
        "uuid": r"[0-9a-fA-F-]+",
        "float": r"\d+(?:\.\d+)?",
    }

    # Escape regex special characters in static parts
    def escape_static(text: str) -> str:
        return re.escape(text)

    # Pattern to find <converter:name> or <name>
    param_pattern = re.compile(r"<(?:(?P<conv>\w+):)?(?P<name>\w+)>")

    # Build the regex piece by piece
    regex_parts = []
    last_end = 0

    for match in param_pattern.finditer(path):
        start, end = match.span()
        # Add static part before the parameter
        if start > last_end:
            static_part = path[last_end:start]
            regex_parts.append(escape_static(static_part))

        conv = match.group("conv") or "str"
        name = match.group("name")
        pattern = converter_map.get(conv, converter_map["str"])
        # Use named capturing group
        regex_parts.append(f"(?P<{name}>{pattern})")

        last_end = end

    # Add any trailing static part
    if last_end < len(path):
        regex_parts.append(escape_static(path[last_end:]))

    # Join parts and anchor
    regex = "^" + "".join(regex_parts) + "$"
    return regex