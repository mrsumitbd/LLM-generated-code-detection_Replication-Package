from typing import Any, Dict

def _process_image_with_tesseract(
    image_path: str,
    config_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Run Tesseract OCR on the given image and return the results.

    Parameters
    ----------
    image_path : str
        Path to the image file to be processed.
    config_dict : dict
        Dictionary of configuration options for Tesseract. Supported keys:
        - "lang" : language code(s) (default: "eng")
        - "psm" : Page Segmentation Mode (default: 3)
        - "oem" : OCR Engine Mode (default: 3)
        - "output_type" : "string" or "dict" (default: "string")
        - "config" : additional config string to pass to Tesseract

    Returns
    -------
    dict
        Dictionary containing the OCR results. Keys:
        - "text" : extracted text (if output_type is "string")
        - "data" : detailed OCR data (if output_type is "dict")
        - "config" : the config_dict used
        - "error" : error message if an exception occurred
    """
    try:
        import pytesseract
        from PIL import Image
    except Exception as exc:
        return {"error": f"Required libraries not available: {exc}"}

    # Build the Tesseract config string
    lang = config_dict.get("lang", "eng")
    psm = config_dict.get("psm", 3)
    oem = config_dict.get("oem", 3)
    extra_cfg = config_dict.get("config", "")
    tesseract_cfg = f"-l {lang} --psm {psm} --oem {oem} {extra_cfg}".strip()

    output_type = config_dict.get("output_type", "string").lower()

    try:
        img = Image.open(image_path)
    except Exception as exc:
        return {"error": f"Failed to open image: {exc}"}

    try:
        if output_type == "dict":
            data = pytesseract.image_to_data(img, config=tesseract_cfg, output_type=pytesseract.Output.DICT)
            return {"data": data, "config": config_dict}
        else:
            text = pytesseract.image_to_string(img, config=tesseract_cfg)
            return {"text": text, "config": config_dict}
    except Exception as exc:
        return {"error": f"OCR processing failed: {exc}"}