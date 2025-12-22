from pathlib import Path
from typing import Literal

def _classify(path: Path) -> Literal["raster", "vector", "other"]:
    if path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        return "raster"
    elif path.suffix.lower() in ['.shp', '.geojson', '.kml', '.gpx']:
        return "vector"
    else:
        return "other"