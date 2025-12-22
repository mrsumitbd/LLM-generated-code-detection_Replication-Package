from msgspec import MsgspecError
import msgspec

def deserialize(value: str | bytes, target_type: type[T], json: bool = False) -> T:
    decoder = msgspec.json.decode if json else msgspec.msgpack.decode

    if json:
        data = value.encode() if isinstance(value, str) else value
    else:
        data = value.encode() if isinstance(value, str) else value

    try:
        return decoder(data, type=target_type, strict=False)
    except MsgspecError as e:
        raise ValueError(f"Failed to deserialize to {target_type.__name__}: {e}") from e