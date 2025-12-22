
class ImageDublicator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "count": ("INT", {"default": 1, "min": 0}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGES",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "execute"
    CATEGORY = "🌌 ReActor"

    def execute(self, image, count):
        images = [image for i in range(count)]
        return (images,)