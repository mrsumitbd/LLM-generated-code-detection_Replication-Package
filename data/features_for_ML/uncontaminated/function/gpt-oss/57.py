def pil_to_tensor(image):
    import numpy as np
    # Convert PIL image to a NumPy array
    arr = np.array(image)
    # Ensure the array has a channel dimension
    if arr.ndim == 2:          # grayscale image
        arr = np.expand_dims(arr, axis=-1)
    # Convert to float32 and normalize to [0, 1]
    arr = arr.astype(np.float32) / 255.0
    # Add a batch dimension: shape becomes [1, height, width, channels]
    arr = np.expand_dims(arr, axis=0)
    return arr