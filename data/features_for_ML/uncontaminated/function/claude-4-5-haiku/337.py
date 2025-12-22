def get_weight(self) -> float:
    """Get current weight reading (读数)
    
    Returns:
        float: Weight value
    """
    if not hasattr(self, '_weight'):
        self._weight = 0.0
    return self._weight