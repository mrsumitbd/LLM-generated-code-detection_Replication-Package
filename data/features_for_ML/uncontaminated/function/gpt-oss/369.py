def INPUT_TYPES(s):
    """
    Defines the input types and tooltips for the node.

    Parameters
    ----------
    s : str
        The name of the required input field.

    Returns
    -------
    dict
        A dictionary specifying the required inputs and their descriptions for the node interface.
    """
    return {
        "required": {
            s: {
                "type": "string",
                "tooltip": f"Enter {s}"
            }
        },
        "optional": {
            "output": {
                "type": "string",
                "tooltip": "Output string"
            }
        }
    }