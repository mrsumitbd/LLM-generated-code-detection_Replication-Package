import httpx
import contextlib

def extract_messages(exc):
    if isinstance(exc, BaseExceptionGroup):
        return [(exc_type, msg) for e in exc.exceptions for exc_type, msg in extract_messages(e)]
    else:
        message = str(exc)
        if isinstance(exc, httpx.HTTPStatusError):
            with contextlib.suppress(Exception):
                message = str(exc).split(" for url", maxsplit=1)[0]
                message = f"{message}: {exc.response.json()['detail']}"

        return [(type(exc).__name__, message)]