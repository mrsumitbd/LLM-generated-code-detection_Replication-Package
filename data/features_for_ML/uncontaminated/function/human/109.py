import chardet

def try_ensure_utf8(data: bytes) -> bytes:
    """
    Try to ensure that the given data is encoded in UTF-8.

    Parameters:
        data: Input data that may or may not yet be UTF-8 or another encoding.

    Returns the input data encoded in UTF-8 if successful. If unable to detect the
    encoding of the input data, then the original data is returned as-received.
    """
    try:
        data.decode("utf8")
        return data
    except UnicodeDecodeError:
        try:
            # CP-1252 is a superset of latin1 but has gaps. Replace unknown
            # characters instead of failing on them.
            return data.decode("cp1252", errors="replace").encode("utf8")
        except UnicodeDecodeError:
            try:
                # last ditch effort to detect encoding
                detection_result = chardet.detect(data)
                if not detection_result["encoding"]:
                    return data
                return data.decode(detection_result["encoding"]).encode("utf8")
            except UnicodeDecodeError:
                return data