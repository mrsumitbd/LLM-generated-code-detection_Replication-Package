import os
import pytesseract
from PIL import Image

def _process_image_with_tesseract(
    image_path: str,
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, config=config_dict)
        return {"text": text.strip()}
    except Exception as e:
        error_message = f"Error processing image at {image_path}: {str(e)}"
        return {"error": error_message}