import os
from pathlib import Path
from typing import Any, Union
from fastmcp.context import Context
from fastmcp.exceptions import ToolError
import geopandas as gpd

def clip(
    input_path: str,
    output_path: str | Path,
    bounds: list[float] | None = None,
    mask: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Clip a vector dataset by bounding box or mask geometry.

    Args:
        input_path: Path to source vector dataset
        output_path: Path for output vector file
        bounds: Optional bounding box [minx, miny, maxx, maxy]
        mask: Optional path to mask geometry file
        ctx: Optional FastMCP context for logging

    Returns:
        Dictionary with clipping metadata:
        - feature_count: Number of features in output
        - geometry_type: Primary geometry type
        - bounds: Output spatial extent
        - clip_method: "bbox" or "mask"

    Raises:
        ToolError: If clipping fails or neither bounds nor mask provided
    """
    if not bounds and not mask:
        raise ToolError("Either bounds or mask must be provided.")

    input_gdf = gpd.read_file(input_path)

    if bounds:
        input_gdf = input_gdf.cx[bounds[0]:bounds[2], bounds[1]:bounds[3]]
        clip_method = "bbox"
    else:
        mask_gdf = gpd.read_file(mask)
        input_gdf = gpd.clip(input_gdf, mask_gdf)
        clip_method = "mask"

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    input_gdf.to_file(output_path)

    return {
        "feature_count": len(input_gdf),
        "geometry_type": input_gdf.geom_type.iloc[0],
        "bounds": input_gdf.total_bounds.tolist(),
        "clip_method": clip_method,
    }