import pytesseract
from PIL import Image
from typing import Any


def _process_image_with_tesseract(
    image_path: str,
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Process an image with Tesseract OCR and return the results.
    
    Args:
        image_path: Path to the image file
        config_dict: Configuration dictionary for Tesseract
        
    Returns:
        Dictionary containing OCR results
    """
    image = Image.open(image_path)
    
    config_string = ""
    if config_dict:
        for key, value in config_dict.items():
            if isinstance(value, bool):
                if value:
                    config_string += f"--{key} "
            else:
                config_string += f"--{key} {value} "
    
    text = pytesseract.image_to_string(image, config=config_string.strip())
    
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=config_string.strip())
    
    return {
        "text": text,
        "data": data,
        "image_path": image_path,
        "config": config_dict
    }