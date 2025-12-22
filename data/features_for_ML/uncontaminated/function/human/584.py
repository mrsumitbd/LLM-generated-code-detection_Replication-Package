import cv2
import numpy as np

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
    # Compare under hsv
    scene_hsv = cv2.cvtColor(scene_orig, cv2.COLOR_BGR2HSV)

    lower_green_hsv_threshold = np.array([30, 100, 210])
    upper_green_hsv_threshold = np.array([55, 160, 255])


    green_mask = cv2.inRange(scene_hsv, lower_green_hsv_threshold, upper_green_hsv_threshold)

    scene_gray = cv2.cvtColor(scene_orig, cv2.COLOR_BGR2GRAY)
    scene_canny_edges = cv2.Canny(scene_gray, canny_low_threshold, canny_high_threshold)

    combined_scene_edges = cv2.bitwise_and(scene_canny_edges, scene_canny_edges, mask=green_mask)
    
    template_border_gray = cv2.cvtColor(template_border_color, cv2.COLOR_BGR2GRAY)
    template_edges = cv2.Canny(template_border_gray, canny_low_threshold, canny_high_threshold)

    result = cv2.matchTemplate(combined_scene_edges, template_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val > match_threshold, max_val, max_loc