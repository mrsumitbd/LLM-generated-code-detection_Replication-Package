import cv2
import numpy as np

def combined_color_canny_matching(template_border_color, scene_orig,
                                  canny_low_threshold=50, canny_high_threshold=150,
                                  match_threshold=0.7):
    """
    Args:
        template_border_color (np.array): shield image array (template)
        scene_orig (np.array): target scene image array
        canny_low_threshold (int): Canny low threshold.
        canny_high_threshold (int): Canny high threshold.
        match_threshold (float): Template matching similarity threshold (0.0-1.0).
    Returns:
        tuple: (is_found, confidence, location)
            is_found (bool): True if match found above threshold.
            confidence (float): Best matching score.
            location (tuple): (x, y) top-left corner of best match in scene.
    """
    # Validate inputs
    if template_border_color is None or scene_orig is None:
        return False, 0.0, None

    # Convert to grayscale
    template_gray = cv2.cvtColor(template_border_color, cv2.COLOR_BGR2GRAY)
    scene_gray = cv2.cvtColor(scene_orig, cv2.COLOR_BGR2GRAY)

    # Edge detection
    template_edges = cv2.Canny(template_gray, canny_low_threshold, canny_high_threshold)
    scene_edges = cv2.Canny(scene_gray, canny_low_threshold, canny_high_threshold)

    # Template matching
    res = cv2.matchTemplate(scene_edges, template_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Determine if match is good enough
    is_found = max_val >= match_threshold
    confidence = max_val
    location = max_loc if is_found else None

    return is_found, confidence, location