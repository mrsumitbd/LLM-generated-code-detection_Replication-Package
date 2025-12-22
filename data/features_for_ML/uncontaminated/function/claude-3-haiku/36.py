import base64
import io
from PIL import Image

def preprocess_image(b64_image):
    """
    Preprocesses an image in base64 format.
    
    Args:
        b64_image (str): The base64-encoded image.
    
    Returns:
        numpy.ndarray: The preprocessed image as a NumPy array.
    """
    # Decode the base64 image
    image_bytes = base64.b64decode(b64_image)
    
    # Load the image using Pillow
    image = Image.open(io.BytesIO(image_bytes))
    
    # Resize the image to a fixed size
    image = image.resize((224, 224))
    
    # Convert the image to a NumPy array
    image_array = np.array(image)
    
    # Normalize the pixel values to the range [0, 1]
    image_array = image_array / 255.0
    
    return image_array