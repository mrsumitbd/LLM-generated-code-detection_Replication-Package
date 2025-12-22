def rgb2ycbcr_pt(img, y_only=False):
    r = img[:, 0, :, :]
    g = img[:, 1, :, :]
    b = img[:, 2, :, :]

    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 0.564 * (b - y)
    cr = 0.713 * (r - y)

    if y_only:
        return y.unsqueeze(1)
    else:
        return torch.stack((y, cb, cr), dim=1)