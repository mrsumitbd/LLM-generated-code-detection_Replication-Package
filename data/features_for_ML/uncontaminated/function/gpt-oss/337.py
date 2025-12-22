def get_weight(self) -> float:
    """Get current weight reading (读数)

    Returns:
        float: Weight value
    """
    # Attempt to read from a sensor object if available
    if hasattr(self, "_sensor") and hasattr(self._sensor, "read_weight"):
        try:
            return float(self._sensor.read_weight())
        except Exception:
            pass

    # Fallback to an internal attribute if set
    if hasattr(self, "_weight"):
        return float(self._weight)

    # If no source is available, raise an informative error
    raise RuntimeError("No weight source available")