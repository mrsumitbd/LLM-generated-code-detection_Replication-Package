import base64
from io import BytesIO
from PIL import Image

def preprocess_image(b64_image):
    image_data = base64.b64decode(b64_image)
    image = Image.open(BytesIO(image_data))
    image = image.resize((224, 224))
    return image