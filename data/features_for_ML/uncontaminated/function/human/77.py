from pathlib import Path
from typing import Any, Literal

def _classify(path: Path) -> Literal["raster", "vector", "other"]:
    suffix = path.suffix.lower()
    if suffix in RASTER_EXTENSIONS:
        return "raster"
    if suffix in VECTOR_EXTENSIONS:
        return "vector"
    if suffix == ".zip":
        # Heuristic: zipped shapefile/geopackage
        lower_name = path.name.lower()
        if any(token in lower_name for token in ("shapefile", "vector", "gpkg")):
            return "vector"
    return "other"