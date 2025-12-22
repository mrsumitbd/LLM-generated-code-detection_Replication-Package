def INPUT_TYPES(s):
    return {
        "required": {
            "text": ("STRING", {"multiline": True}),
            "font": (folder_paths.get_filename_list("fonts"),),
            "size": ("INT", {"default": 28, "min": 1, "max": 500}),
            "color": ("STRING", {"default": "#000000"}),
            "background_color": ("STRING", {"default": "#FFFFFF"}),
            "margin": ("INT", {"default": 10, "min": 0, "max": 500}),
            "line_spacing": ("INT", {"default": 0, "min": -100, "max": 100}),
        },
        "optional": {
            "alignment": (["left", "center", "right"],),
        }
    }