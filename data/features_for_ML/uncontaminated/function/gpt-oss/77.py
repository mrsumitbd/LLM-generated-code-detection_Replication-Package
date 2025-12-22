from pathlib import Path
from typing import Literal

def _classify(path: Path) -> Literal["raster", "vector", "other"]:
    """
    Classify a file as raster, vector, or other based on its extension.

    Parameters
    ----------
    path : Path
        Path to the file to classify.

    Returns
    -------
    Literal["raster", "vector", "other"]
        Classification of the file.
    """
    # Define known raster and vector extensions (case‑insensitive)
    raster_exts = {
        ".tif", ".tiff", ".img", ".asc", ".grd", ".vrt", ".nc", ".hdf", ".h5", ".hdf5",
        ".jp2", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".gif", ".tga", ".dds",
    }
    vector_exts = {
        ".shp", ".geojson", ".json", ".gpkg", ".kml", ".gml", ".xml", ".csv",
        ".txt", ".tab", ".dxf", ".dwg", ".prj",
    }

    ext = path.suffix.lower()
    if ext in raster_exts:
        return "raster"
    if ext in vector_exts:
        return "vector"
    return "other"