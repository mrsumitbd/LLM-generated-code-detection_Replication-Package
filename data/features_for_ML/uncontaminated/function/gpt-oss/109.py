def try_ensure_utf8(data: bytes) -> bytes:
    """
    Try to ensure that the given data is encoded in UTF-8.

    Parameters:
        data: Input data that may or may not yet be UTF-8 or another encoding.

    Returns the input data encoded in UTF-8 if successful. If unable to detect the
    encoding of the input data, then the original data is returned as-received.
    """
    if not data:
        return data

    # First, try decoding as UTF-8 directly
    try:
        data.decode("utf-8")
        return data
    except UnicodeDecodeError:
        pass

    # Common encodings to try
    encodings = [
        "latin-1",
        "iso-8859-1",
        "cp1252",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        "utf-32",
        "utf-32-le",
        "utf-32-be",
        "shift_jis",
        "gbk",
        "euc-kr",
        "big5",
        "iso-2022-jp",
        "iso-2022-kr",
        "windows-1251",
        "windows-1250",
        "windows-1253",
        "windows-1254",
        "windows-1255",
        "windows-1256",
        "windows-1257",
        "windows-1258",
    ]

    for enc in encodings:
        try:
            text = data.decode(enc)
            # Re-encode to UTF-8
            return text.encode("utf-8")
        except UnicodeDecodeError:
            continue

    # If all attempts fail, return the original data
    return data