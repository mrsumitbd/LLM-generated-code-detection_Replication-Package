from typing import Literal

# Assume HTMLOutput is defined elsewhere in the package.
# Import it here. If it's in the same module, adjust the import accordingly.
try:
    from .output import HTMLOutput  # type: ignore
except Exception:
    # Fallback: define a minimal placeholder for type checking purposes.
    class HTMLOutput:
        def __init__(self, layout: str):
            self.layout = layout

        def __repr__(self):
            return f"<HTMLOutput layout={self.layout!r}>"

def html(layout: Literal["page", "reflow"]) -> HTMLOutput:
    """
    HTML output configuration.

    Args:
        layout: The layout type to use for conversion to HTML

    Returns:
        HTMLOutput object
    """
    if layout not in {"page", "reflow"}:
        raise ValueError(f"layout must be 'page' or 'reflow', got {layout!r}")

    return HTMLOutput(layout=layout)