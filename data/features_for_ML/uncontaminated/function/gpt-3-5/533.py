def _process_image_with_tesseract(image_path: str, config_dict: dict[str, Any]) -> dict[str, Any]:
    # Your implementation here
    import pytesseract
    from PIL import Image

    image = Image.open(image_path)
    custom_config = config_dict
    text = pytesseract.image_to_string(image, config=custom_config)

    result = {
        "text": text
    }

    return result