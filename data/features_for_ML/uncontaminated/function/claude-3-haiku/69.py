def check_input_image(input_image):
    import os
    import cv2
    import numpy as np

    # Check if the input is a valid file path
    if not os.path.isfile(input_image):
        return False, "Input is not a valid file path."

    # Load the image using OpenCV
    try:
        img = cv2.imread(input_image)
    except cv2.error as e:
        return False, f"Error loading the image: {e}"

    # Check if the image was loaded successfully
    if img is None:
        return False, "Failed to load the image."

    # Check the image dimensions
    if len(img.shape) != 3 or img.shape[2] != 3:
        return False, "Input image must be a 3-channel RGB image."

    # Check the image size
    if img.shape[0] < 32 or img.shape[1] < 32:
        return False, "Input image must be at least 32x32 pixels."

    # Check the image data type
    if img.dtype != np.uint8:
        return False, "Input image must have a data type of uint8."

    # If all checks pass, return True and an empty message
    return True, ""