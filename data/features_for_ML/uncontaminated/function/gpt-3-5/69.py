def check_input_image(input_image):
    if not isinstance(input_image, str):
        return False
    if not input_image.endswith('.jpg') and not input_image.endswith('.jpeg') and not input_image.endswith('.png'):
        return False
    return True