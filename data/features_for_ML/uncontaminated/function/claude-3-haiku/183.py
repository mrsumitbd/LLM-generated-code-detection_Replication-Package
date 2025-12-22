import numpy as np

def resize_landmark(landmark, w, h, new_w, new_h):
    """
    Resizes a landmark array to a new image size.

    Args:
        landmark (np.ndarray): A 2D numpy array of shape (N, 2) representing the landmark coordinates.
        w (int): The width of the original image.
        h (int): The height of the original image.
        new_w (int): The new width of the image.
        new_h (int): The new height of the image.

    Returns:
        np.ndarray: The resized landmark array of shape (N, 2).
    """
    scale_x = new_w / w
    scale_y = new_h / h
    resized_landmark = np.zeros_like(landmark)
    resized_landmark[:, 0] = landmark[:, 0] * scale_x
    resized_landmark[:, 1] = landmark[:, 1] * scale_y
    return resized_landmark