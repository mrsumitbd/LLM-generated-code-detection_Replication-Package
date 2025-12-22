import base64
import io
from PIL import Image
import numpy as np

def preprocess_image(b64_image):
    """
    Decode a base64-encoded image, convert it to RGB, resize to 224x224,
    and return a NumPy array normalized to the range [0, 1].

    Parameters
    ----------
    b64_image : str
        Base64-encoded image string.

    Returns
    -------
    np.ndarray
        Preprocessed image array of shape (224, 224, 3) with dtype float32.
    """
    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(b64_image)

    # Load the image with Pillow
    with io.BytesIO(image_bytes) as buf:
        img = Image.open(buf).convert("RGB")

    # Resize to 224x224 (common size for many CNNs)
    img = img.resize((224, 224), Image.BILINEAR)

    # Convert to NumPy array and normalize to [0, 1]
    img_array = np.asarray(img, dtype=np.float32) / 255.0

    return img_array