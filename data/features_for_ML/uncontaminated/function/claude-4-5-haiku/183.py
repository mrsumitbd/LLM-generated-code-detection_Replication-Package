def resize_landmark(landmark, w, h, new_w, new_h):
    """
    Resize landmark coordinates from original image dimensions to new dimensions.
    
    Args:
        landmark: List of [x, y] coordinates or a single [x, y] coordinate
        w: Original image width
        h: Original image height
        new_w: New image width
        new_h: New image height
    
    Returns:
        Resized landmark(s) with same structure as input
    """
    if not landmark:
        return landmark
    
    # Check if landmark is a list of coordinates or a single coordinate
    if isinstance(landmark[0], (list, tuple)):
        # Multiple landmarks
        return [[x * new_w / w, y * new_h / h] for x, y in landmark]
    else:
        # Single landmark
        return [landmark[0] * new_w / w, landmark[1] * new_h / h]