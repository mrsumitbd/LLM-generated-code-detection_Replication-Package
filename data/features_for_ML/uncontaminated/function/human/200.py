def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "count": ("INT", {"default": 1, "min": 0}),
            },
        }