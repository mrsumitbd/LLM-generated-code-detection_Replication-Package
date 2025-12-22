import cv2
import numpy as np

def find_pattern_sqdiff(
        img, img_pattern,
        last_result=None,
        mask=None,
        local_search_radius=50,
        global_threshold=0.4
    ):
    '''
    Perform masked template matching using SQDIFF_NORMED method.

    The function searches for the best matching location of img_pattern inside img.
    It automatically converts the pattern to grayscale and generates a mask to ignore
    pure white (or near-white) pixels in the template, treating them as transparent background.

    Parameters:
    - img: Target search image (numpy array), can be grayscale or BGR.
    - img_pattern: Template image to search for (numpy array, BGR).

    Returns:
    - min_loc: The top-left coordinate (x, y) of the best match position.
    - min_val: The matching score (lower = better for SQDIFF_NORMED).
    - bool: local search success or not
    '''
    # Convert the pattern to grayscale
    img_pattern_gray = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY)

    # Generate a mask to ignore pure white (or near-white) pixels in the template
    if mask is None:
        mask = cv2.inRange(img_pattern_gray, 250, 255)

    # Perform template matching using SQDIFF_NORMED method
    if last_result is None:
        res = cv2.matchTemplate(img, img_pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    else:
        # Perform local search around the last result
        x, y = last_result
        local_search_img = img[max(0, y - local_search_radius):min(img.shape[0], y + local_search_radius + 1),
                           max(0, x - local_search_radius):min(img.shape[1], x + local_search_radius + 1)]
        local_search_res = cv2.matchTemplate(local_search_img, img_pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(local_search_res)
        min_loc = (min_loc[0] + max(0, x - local_search_radius), min_loc[1] + max(0, y - local_search_radius))

    # Check if the match is good enough
    if min_val < global_threshold:
        return min_loc, min_val, True
    else:
        return None, None, False