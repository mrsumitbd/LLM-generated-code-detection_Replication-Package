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
    # 1. 对场景图像进行Canny边缘检测
    scene_canny = cv2.Canny(scene_orig, canny_low_threshold, canny_high_threshold)

    # 2. 对模板图像进行Canny边缘检测
    template_canny = cv2.Canny(template_border_color, canny_low_threshold, canny_high_threshold)

    # 3. 使用模板匹配算法在场景图像中查找模板
    res = cv2.matchTemplate(scene_canny, template_canny, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 4. 判断是否找到匹配的目标
    is_found = max_val >= match_threshold
    confidence = max_val
    location = max_loc if is_found else None

    return is_found, confidence, location