def format_alert(feature: dict) -> str:
    """
    Format an alert feature into a readable string.

    The function expects a GeoJSON‑style feature dictionary with at least the
    following structure:

        {
            "type": "Feature",
            "properties": {
                "alert_type": str,
                "severity": str,
                "description": str,
                "timestamp": str,   # ISO 8601 or any human‑readable string
                ...                # other optional keys
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat, ...]
            }
        }

    The returned string contains the most important information in a
    human‑friendly format.  Missing keys are simply omitted.

    Parameters
    ----------
    feature : dict
        The feature dictionary to format.

    Returns
    -------
    str
        A formatted string representation of the alert.
    """
    # Extract properties safely
    props = feature.get("properties", {})
    alert_type = props.get("alert_type") or props.get("type") or "Unknown type"
    severity = props.get("severity") or "Unknown severity"
    description = props.get("description") or "No description provided."
    timestamp = props.get("timestamp") or props.get("time") or "Unknown time"

    # Extract geometry safely
    geometry = feature.get("geometry", {})
    coords = geometry.get("coordinates")
    if isinstance(coords, (list, tuple)):
        # Convert coordinates to a readable string
        coord_str = ", ".join(f"{c:.4f}" for c in coords)
    else:
        coord_str = "Unknown location"

    # Build the formatted string
    lines = [
        f"Alert: {alert_type} ({severity})",
        f"Time: {timestamp}",
        f"Description: {description}",
        f"Location: {coord_str}",
    ]

    return "\n".join(lines)