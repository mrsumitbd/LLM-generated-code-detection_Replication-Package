def INPUT_TYPES(s):
        return {
            "required": {
                "input_image": ("IMAGE",),
                "faceswap_weight": (["0%", "12.5%", "25%", "37.5%", "50%", "62.5%", "75%", "87.5%", "100%"], {"default": "50%"}),
            },
            "optional": {
                "source_image": ("IMAGE",),
                "face_model": ("FACE_MODEL",),
            }
        }