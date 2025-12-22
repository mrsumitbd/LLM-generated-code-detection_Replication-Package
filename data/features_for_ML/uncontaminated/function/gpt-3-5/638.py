from pathlib import Path
from typing import Any, Union
from fastmcp import Context

def clip(
    input_path: str,
    output_path: Union[str, Path],
    bounds: Union[list[float], None] = None,
    mask: Union[str, None] = None,
    ctx: Union[Context, None] = None,
) -> dict[str, Any]:
    pass