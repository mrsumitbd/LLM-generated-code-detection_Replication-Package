def bgr_to_rgb(tensor_img):
    tensor_img = tensor_img.flip(0)
    return tensor_img