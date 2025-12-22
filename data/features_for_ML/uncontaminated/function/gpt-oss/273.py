def _add_terminate(r: "Resource"):
    """
    Ensure the given resource instance has a `terminate` method.

    If the resource already defines `terminate`, nothing is changed.
    Otherwise, if it defines a `close` or `shutdown` method, that method
    is aliased as `terminate`.  If neither is present, a no‑op
    `terminate` method is added.

    This helper is useful for normalising resource cleanup across
    different types of objects.
    """
    # If the resource already has a terminate method, do nothing.
    if hasattr(r, "terminate"):
        return

    # Prefer close() if available.
    if hasattr(r, "close") and callable(getattr(r, "close")):
        r.terminate = r.close
    # Fallback to shutdown() if close() is not present.
    elif hasattr(r, "shutdown") and callable(getattr(r, "shutdown")):
        r.terminate = r.shutdown
    # If no suitable method exists, provide a harmless no‑op.
    else:
        def _noop(*args, **kwargs):
            """A no‑op terminate implementation."""
            return None

        r.terminate = _noop