import cv2
import numpy as np

def combined_color_canny_matching(template_border_color, scene_orig,
                                  canny_low_threshold=50, canny_high_threshold=150,
                                  match_threshold=0.7):
    
    def canny_edge_detection(image, low_threshold, high_threshold):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        return edges

    template_edges = canny_edge_detection(template_border_color, canny_low_threshold, canny_high_threshold)
    scene_edges = canny_edge_detection(scene_orig, canny_low_threshold, canny_high_threshold)

    res = cv2.matchTemplate(scene_edges, template_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= match_threshold:
        is_found = True
        confidence = max_val
        location = max_loc
    else:
        is_found = False
        confidence = 0
        location = (0, 0)

    return is_found, confidence, location