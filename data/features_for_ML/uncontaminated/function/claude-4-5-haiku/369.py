def INPUT_TYPES(s):
    """
    Defines the input types and tooltips for the node.

    Returns
    -------
    dict
        A dictionary specifying the required inputs and their descriptions for the node interface.
    """
    return {
        "required": {
            "text": ("STRING", {
                "multiline": True,
                "default": ""
            }),
        },
        "optional": {
            "extra": ("STRING", {
                "multiline": False,
                "default": ""
            }),
        }
    }