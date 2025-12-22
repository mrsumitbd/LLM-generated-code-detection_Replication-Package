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
    import cv2
    import numpy as np
    
    # Convert img to grayscale if needed
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    
    # Convert pattern to grayscale
    if len(img_pattern.shape) == 3:
        pattern_gray = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY)
    else:
        pattern_gray = img_pattern
    
    # Generate mask if not provided - ignore near-white pixels
    if mask is None:
        # Create mask from pattern - white/near-white pixels are ignored
        mask = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY) if len(img_pattern.shape) == 3 else img_pattern
        mask = cv2.inRange(mask, 0, 240)  # Ignore pixels with value > 240 (near-white)
    
    # Perform template matching with mask
    result = cv2.matchTemplate(img_gray, pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask)
    
    min_val = np.min(result)
    min_loc = np.unravel_index(np.argmin(result), result.shape)
    min_loc = (min_loc[1], min_loc[0])  # Convert to (x, y)
    
    local_search_success = False
    
    # Try local search if last result is available
    if last_result is not None:
        last_x, last_y = last_result
        
        # Define local search region
        search_top = max(0, last_y - local_search_radius)
        search_left = max(0, last_x - local_search_radius)
        search_bottom = min(img_gray.shape[0], last_y + local_search_radius + img_pattern.shape[0])
        search_right = min(img_gray.shape[1], last_x + local_search_radius + img_pattern.shape[1])
        
        # Extract search region
        if search_bottom > search_top and search_right > search_left:
            img_region = img_gray[search_top:search_bottom, search_left:search_right]
            
            # Perform local template matching
            if img_region.shape[0] >= pattern_gray.shape[0] and img_region.shape[1] >= pattern_gray.shape[1]:
                local_result = cv2.matchTemplate(img_region, pattern_gray, cv2.TM_SQDIFF_NORMED, mask=mask)
                local_min_val = np.min(local_result)
                
                # Use local result if it's better and within threshold
                if local_min_val < min_val and local_min_val < global_threshold:
                    local_min_loc = np.unravel_index(np.argmin(local_result), local_result.shape)
                    min_loc = (local_min_loc[1] + search_left, local_min_loc[0] + search_top)
                    min_val = local_min_val
                    local_search_success = True
    
    return min_loc, min_val, local_search_success