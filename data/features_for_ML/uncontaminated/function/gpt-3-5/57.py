import numpy as np
import tensorflow as tf

def pil_to_tensor(image):
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
    return image_tensor