from io import BytesIO
from PIL import Image
import base64

def preprocess_image(b64_image):
    image_bytes = base64.b64decode(b64_image)
    image_buffer = BytesIO(image_bytes)
    pil_image = Image.open(image_buffer)
    return base_transforms(pil_image)