import copy
import numpy as np
from PIL import Image


class ImageDublicator:
    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types for the node.
        Returns a dictionary with required inputs:
        - image: an image object (PIL.Image.Image, numpy.ndarray, or any object that can be copied)
        - count: integer number of times to duplicate the image (default 2, min 1)
        """
        return {
            "required": {
                "image": ("IMAGE",),
                "count": ("INT", {"default": 2, "min": 1}),
            }
        }

    def execute(self, image, count):
        """
        Duplicate the given image `count` times.

        Parameters
        ----------
        image : PIL.Image.Image | numpy.ndarray | any
            The image to duplicate.
        count : int
            Number of duplicates to produce.

        Returns
        -------
        list
            A list containing `count` copies of the input image.
        """
        # Validate count
        try:
            count = int(count)
        except Exception:
            raise ValueError(f"count must be an integer, got {count!r}")

        if count < 1:
            raise ValueError(f"count must be >= 1, got {count}")

        # Helper to copy image safely
        def _copy_img(img):
            # PIL Image
            if isinstance(img, Image.Image):
                return img.copy()
            # NumPy array
            if isinstance(img, np.ndarray):
                return np.copy(img)
            # Generic copy via copy module
            try:
                return copy.deepcopy(img)
            except Exception:
                # Fallback: return the same reference
                return img

        return [_copy_img(image) for _ in range(count)]