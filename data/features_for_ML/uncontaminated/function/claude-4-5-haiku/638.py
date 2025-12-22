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
    import geopandas as gpd
    from pathlib import Path
    
    if bounds is None and mask is None:
        raise ToolError("Either bounds or mask must be provided")
    
    try:
        output_path = Path(output_path)
        
        # Read input dataset
        gdf = gpd.read_file(input_path)
        
        if gdf.empty:
            raise ToolError("Input dataset is empty")
        
        clip_method = None
        
        # Clip by bounding box
        if bounds is not None:
            if len(bounds) != 4:
                raise ToolError("Bounds must be [minx, miny, maxx, maxy]")
            
            minx, miny, maxx, maxy = bounds
            
            from shapely.geometry import box
            bbox = box(minx, miny, maxx, maxy)
            clipped_gdf = gpd.clip(gdf, bbox)
            clip_method = "bbox"
        
        # Clip by mask geometry
        elif mask is not None:
            mask_gdf = gpd.read_file(mask)
            
            if mask_gdf.empty:
                raise ToolError("Mask dataset is empty")
            
            # Merge mask geometries if multiple features
            mask_geom = mask_gdf.unary_union
            clipped_gdf = gpd.clip(gdf, mask_geom)
            clip_method = "mask"
        
        if clipped_gdf.empty:
            raise ToolError("Clipping resulted in empty dataset")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write output
        clipped_gdf.to_file(output_path)
        
        # Get geometry type
        geom_types = clipped_gdf.geometry.type.unique()
        geometry_type = geom_types[0] if len(geom_types) > 0 else "Unknown"
        
        # Get bounds
        bounds_result = clipped_gdf.total_bounds.tolist()
        
        result = {
            "feature_count": len(clipped_gdf),
            "geometry_type": geometry_type,
            "bounds": bounds_result,
            "clip_method": clip_method,
        }
        
        if ctx:
            ctx.log(f"Successfully clipped {len(clipped_gdf)} features using {clip_method}")
        
        return result
        
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Clipping failed: {str(e)}")