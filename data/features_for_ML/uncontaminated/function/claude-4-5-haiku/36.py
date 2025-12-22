import base64
import io
from PIL import Image
import numpy as np

def preprocess_image(b64_image):
    """
    Preprocess a base64-encoded image for use with Claude's vision capabilities.
    
    Args:
        b64_image: A base64-encoded image string
        
    Returns:
        A dictionary with 'type' and 'image_data' keys suitable for Claude's API
    """
    # Decode the base64 image
    image_data = base64.b64decode(b64_image)
    
    # Open the image with PIL
    image = Image.read(io.BytesIO(image_data))
    
    # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize if image is too large (Claude has size limits)
    max_dimension = 1024
    if image.width > max_dimension or image.height > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    
    # Convert back to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)
    processed_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": processed_b64
        }
    }