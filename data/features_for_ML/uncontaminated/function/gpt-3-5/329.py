import numpy as np

def rgb2ycbcr(img, y_only=False):
    if img.dtype == np.uint8:
        img = img.astype(np.float32) / 255.0

    ycbcr = np.empty_like(img)
    ycbcr[..., 0] = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]
    ycbcr[..., 1] = 0.564 * (img[..., 2] - ycbcr[..., 0])
    ycbcr[..., 2] = 0.713 * (img[..., 0] - ycbcr[..., 0])

    if y_only:
        return ycbcr[..., 0]
    else:
        return ycbcr