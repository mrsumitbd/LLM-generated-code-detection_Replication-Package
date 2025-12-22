class ImageDublicator:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "count": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 16,
                    "step": 1
                }),
            },
        }

    def execute(self, image, count):
        duplicated_images = [image] * count
        result = tuple(duplicated_images)
        return result