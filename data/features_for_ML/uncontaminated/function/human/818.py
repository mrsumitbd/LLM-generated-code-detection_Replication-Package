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
    # Padding if img is smaller than pattern
    img = pad_to_size(img, img_pattern.shape[:2])

    # search last result location first to speedup
    h, w = img_pattern.shape[:2]
    if last_result is not None and global_threshold > 0.0:
        lx, ly = last_result
        x0 = max(0, lx - local_search_radius)
        y0 = max(0, ly - local_search_radius)
        x1 = min(img.shape[1], lx + local_search_radius + w)
        y1 = min(img.shape[0], ly + local_search_radius + h)

        img_roi = img[y0:y1, x0:x1]
        if img_roi.shape[0] >= h and img_roi.shape[1] >= w:
            res = cv2.matchTemplate(
                    img_roi,
                    img_pattern,
                    cv2.TM_SQDIFF_NORMED,
                    mask=mask
            )
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if min_val < global_threshold:
                return (x0 + min_loc[0], y0 + min_loc[1]), min_val, True

    # Global fallback
    res = cv2.matchTemplate(
            img,
            img_pattern,
            cv2.TM_SQDIFF_NORMED,
            mask=mask
    )

    # Replace -inf/+inf/nan to 1.0 to avoid numerical error
    res = np.nan_to_num(res, nan=1.0, posinf=1.0, neginf=1.0)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return min_loc, min_val, False