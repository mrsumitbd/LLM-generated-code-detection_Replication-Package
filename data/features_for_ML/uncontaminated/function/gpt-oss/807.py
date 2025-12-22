def convert_to_bytes(value, bytes, mock=False):
    """
    Convert a value to a bytes object of a specified length.

    Parameters
    ----------
    value : int | str | bytes
        The value to convert. Integers are converted using two's complement
        representation. Strings are encoded using UTF-8. Bytes are returned
        unchanged.
    bytes : int
        The desired length of the resulting bytes object. For integers this
        determines the number of bytes used in the representation. For
        strings this determines the maximum number of bytes after UTF-8
        encoding. For bytes this argument is ignored.
    mock : bool, optional
        If True, the function returns the original value unchanged. This is
        useful for testing or when the conversion should be skipped.

    Returns
    -------
    bytes
        The converted bytes object.

    Raises
    ------
    TypeError
        If the value type is unsupported.
    OverflowError
        If an integer cannot be represented in the requested number of bytes.
    ValueError
        If the string cannot be encoded within the requested number of bytes.
    """
    if mock:
        return value

    # Handle bytes directly
    if isinstance(value, bytes):
        return value

    # Handle integers
    if isinstance(value, int):
        if bytes <= 0:
            raise ValueError("bytes must be a positive integer")
        # Determine if the integer fits in the requested number of bytes
        # Use signed representation
        try:
            return value.to_bytes(bytes, byteorder="big", signed=True)
        except OverflowError as exc:
            raise OverflowError(
                f"Integer {value} cannot be represented in {bytes} bytes"
            ) from exc

    # Handle strings
    if isinstance(value, str):
        encoded = value.encode("utf-8")
        if len(encoded) > bytes:
            raise ValueError(
                f"Encoded string is {len(encoded)} bytes, "
                f"which exceeds the requested {bytes} bytes"
            )
        # Pad with zeros if necessary
        return encoded.ljust(bytes, b"\x00")

    raise TypeError(f"Unsupported type {type(value).__name__} for conversion")