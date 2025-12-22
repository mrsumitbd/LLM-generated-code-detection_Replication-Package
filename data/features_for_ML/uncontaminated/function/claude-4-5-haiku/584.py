def combined_color_canny_matching(template_border_color, scene_orig,
                                  canny_low_threshold=50, canny_high_threshold=150,
                                  match_threshold=0.7):
    """
    Args:
        template_border_color (np.array): shield image array
        scene_orig (np.array): target scene image array
        canny_low_threshold (int): Canny 边缘检测的低阈值。
        canny_high_threshold (int): Canny 边缘检测的高阈值。
        match_threshold (float): 模板匹配的相似度阈值(0.0-1.0)。
    Returns:
        tuple: (is_found, confidence, location)
    """
    import cv2
    import numpy as np
    
    # Convert to grayscale if needed
    if len(template_border_color.shape) == 3:
        template_gray = cv2.cvtColor(template_border_color, cv2.COLOR_BGR2GRAY)
    else:
        template_gray = template_border_color
    
    if len(scene_orig.shape) == 3:
        scene_gray = cv2.cvtColor(scene_orig, cv2.COLOR_BGR2GRAY)
    else:
        scene_gray = scene_orig
    
    # Apply Canny edge detection
    template_edges = cv2.Canny(template_gray, canny_low_threshold, canny_high_threshold)
    scene_edges = cv2.Canny(scene_gray, canny_low_threshold, canny_high_threshold)
    
    # Template matching on edges
    result = cv2.matchTemplate(scene_edges, template_edges, cv2.TM_CCOEFF_NORMED)
    
    # Find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Use normalized correlation coefficient
    confidence = max_val
    location = max_loc
    
    # Check if match exceeds threshold
    is_found = confidence >= match_threshold
    
    return (is_found, confidence, location)