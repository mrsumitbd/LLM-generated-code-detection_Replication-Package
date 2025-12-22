def reorder_image(img, input_order='HWC'):
    if input_order == 'HWC':
        return img
    elif input_order == 'CHW':
        return img.transpose(1, 2, 0)
    else:
        return img.transpose(0, 1, 2)