import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import geopandas as gpd
from shapely.geometry import box

# Assume these are defined elsewhere in the package
try:
    from fastmcp import Context, ToolError
except ImportError:
    # Minimal stubs for standalone usage
    class Context:
        def log(self, msg: str, level: str = "INFO") -> None:
            logging.log(getattr(logging, level.upper(), logging.INFO), msg)

    class ToolError(Exception):
        pass


def clip(
    input_path: str,
    output_path: Union[str, Path],
    bounds: Optional[List[float]] = None,
    mask: Optional[str] = None,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
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
    ctx = ctx or Context()
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if bounds is None and mask is None:
        raise ToolError("Either bounds or mask must be provided for clipping.")

    try:
        # Read source dataset
        ctx.log(f"Reading input dataset: {input_path}")
        src_gdf = gpd.read_file(input_path)
        if src_gdf.empty:
            raise ToolError("Source dataset is empty.")

        # Perform clipping
        if bounds is not None:
            ctx.log(f"Clipping by bounding box: {bounds}")
            minx, miny, maxx, maxy = bounds
            bbox = box(minx, miny, maxx, maxy)
            clipped_gdf = src_gdf.clip(bbox)
            clip_method = "bbox"
        else:
            ctx.log(f"Clipping by mask geometry: {mask}")
            mask_gdf = gpd.read_file(mask)
            if mask_gdf.empty:
                raise ToolError("Mask dataset is empty.")
            # Ensure same CRS
            if src_gdf.crs != mask_gdf.crs:
                mask_gdf = mask_gdf.to_crs(src_gdf.crs)
            clipped_gdf = gpd.overlay(src_gdf, mask_gdf, how="intersection")
            clip_method = "mask"

        if clipped_gdf.empty:
            ctx.log("Resulting clipped dataset is empty.", level="WARNING")

        # Write output
        ctx.log(f"Writing clipped dataset to: {out_path}")
        clipped_gdf.to_file(out_path, driver=src_gdf.driver)

        # Prepare metadata
        feature_count = len(clipped_gdf)
        geometry_type = (
            clipped_gdf.geometry.type.unique()[0] if not clipped_gdf.empty else None
        )
        bounds_out = (
            clipped_gdf.total_bounds.tolist() if not clipped_gdf.empty else None
        )

        return {
            "feature_count": feature_count,
            "geometry_type": geometry_type,
            "bounds": bounds_out,
            "clip_method": clip_method,
        }

    except Exception as exc:
        ctx.log(f"Clipping failed: {exc}", level="ERROR")
        raise ToolError(f"Clipping failed: {exc}") from exc