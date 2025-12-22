import cv2
import numpy as np

def find_pattern_sqdiff(
        img, img_pattern,
        last_result=None,
        mask=None,
        local_search_radius=50,
        global_threshold=0.4
    ):
    """
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
    """
    # Ensure inputs are numpy arrays
    img = np.asarray(img)
    img_pattern = np.asarray(img_pattern)

    # Convert images to grayscale if needed
    if img.ndim == 3 and img.shape[2] == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img.copy()

    if img_pattern.ndim == 3 and img_pattern.shape[2] == 3:
        pattern_gray = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY)
    else:
        pattern_gray = img_pattern.copy()

    # Create mask if not provided
    if mask is None:
        # Identify near‑white pixels (threshold 250)
        if img_pattern.ndim == 3 and img_pattern.shape[2] == 3:
            white_mask = np.all(img_pattern > 250, axis=2)
        else:
            white_mask = img_pattern > 250
        # Mask: 1 for valid pixels, 0 for ignored
        mask = (~white_mask).astype(np.uint8)

    # If last_result provided, perform local search
    local_search_used = last_result is not None
    if local_search_used:
        # Compute search window around last_result
        x0, y0 = last_result
        h, w = pattern_gray.shape
        # Define window bounds
        x_start = max(x0 - local_search_radius, 0)
        y_start = max(y0 - local_search_radius, 0)
        x_end = min(x0 + local_search_radius + w, img_gray.shape[1])
        y_end = min(y0 + local_search_radius + h, img_gray.shape[0])

        # Crop image and adjust mask accordingly
        img_crop = img_gray[y_start:y_end, x_start:x_end]
        # Adjust mask to crop size
        mask_crop = mask
        # Perform template matching on cropped image
        res = cv2.matchTemplate(img_crop, pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask_crop)
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)
        # Convert local coordinates to original image coordinates
        min_loc = (min_loc[0] + x_start, min_loc[1] + y_start)
    else:
        # Global search
        res = cv2.matchTemplate(img_gray, pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask)
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)

    return min_loc, min_val, local_search_used