from shapely.geometry.base import BaseGeometry
from shapely.affinity import translate

def set_origin_to_geometry(ref=None):
    """
    Translate a Shapely geometry so that its bounding box minimum corner
    becomes the origin (0,0) (or (0,0,0) for 3‑D geometries).

    Parameters
    ----------
    ref : shapely.geometry.base.BaseGeometry
        The geometry to translate.

    Returns
    -------
    shapely.geometry.base.BaseGeometry
        A new geometry translated to the origin.

    Raises
    ------
    ValueError
        If `ref` is None.
    TypeError
        If `ref` is not a Shapely geometry.
    """
    if ref is None:
        raise ValueError("ref must be a Shapely geometry")
    if not isinstance(ref, BaseGeometry):
        raise TypeError("ref must be a Shapely geometry")

    bounds = ref.bounds
    # bounds is a 4‑tuple for 2‑D geometries, 6‑tuple for 3‑D
    if len(bounds) == 4:
        minx, miny, maxx, maxy = bounds
        return translate(ref, xoff=-minx, yoff=-miny)
    else:
        minx, miny, minz, maxx, maxy, maxz = bounds

        def _adjust_coords(geom):
            if geom.is_empty:
                return geom
            if geom.geom_type == "Point":
                return type(geom)(geom.x - minx, geom.y - miny, geom.z - minz)
            if geom.geom_type in ("LineString", "LinearRing"):
                return type(geom)([(x - minx, y - miny, z - minz) for x, y, z in geom.coords])
            if geom.geom_type == "Polygon":
                exterior = _adjust_coords(geom.exterior)
                interiors = [_adjust_coords(ring) for ring in geom.interiors]
                return type(geom)(exterior, interiors)
            # For geometry collections
            return type(geom)([_adjust_coords(part) for part in geom.geoms])

        return _adjust_coords(ref)