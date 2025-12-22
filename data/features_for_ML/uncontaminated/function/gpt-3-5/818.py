import cv2
import numpy as np

def find_pattern_sqdiff(
        img, img_pattern,
        last_result=None,
        mask=None,
        local_search_radius=50,
        global_threshold=0.4
    ):
    
    def preprocess_image(img):
        if len(img.shape) == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img
        img_gray = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX)
        return img_gray

    def preprocess_pattern(img_pattern):
        img_pattern_gray = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img_pattern_gray, 240, 255, cv2.THRESH_BINARY)
        mask = cv2.bitwise_not(mask)
        return img_pattern_gray, mask

    img_gray = preprocess_image(img)
    img_pattern_gray, mask = preprocess_pattern(img_pattern)

    if mask is not None:
        img_pattern_gray = cv2.bitwise_and(img_pattern_gray, mask)

    res = cv2.matchTemplate(img_gray, img_pattern_gray, cv2.TM_SQDIFF_NORMED)
    min_val, _, min_loc, _ = cv2.minMaxLoc(res)

    if min_val > global_threshold:
        return min_loc, min_val, False
    else:
        if last_result is not None:
            x, y = last_result[0]
            x += min_loc[0] - local_search_radius
            y += min_loc[1] - local_search_radius
            x = max(0, min(img_gray.shape[1] - img_pattern_gray.shape[1], x))
            y = max(0, min(img_gray.shape[0] - img_pattern_gray.shape[0], y))
            img_roi = img_gray[y:y+img_pattern_gray.shape[0], x:x+img_pattern_gray.shape[1]]
            res = cv2.matchTemplate(img_roi, img_pattern_gray, cv2.TM_SQDIFF_NORMED)
            min_val, _, min_loc, _ = cv2.minMaxLoc(res)
            min_loc = (min_loc[0] + x, min_loc[1] + y)
            return min_loc, min_val, True
        else:
            return min_loc, min_val, True