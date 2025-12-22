def INPUT_TYPES(s):
    """
    Defines the input types and tooltips for the node.

    Returns
    -------
    dict
        A dictionary specifying the required inputs and their descriptions for the node interface.
    """
    return {
        "input1": {
            "type": "string",
            "tooltip": "Enter the first input string."
        },
        "input2": {
            "type": "number",
            "tooltip": "Enter the second input number."
        },
        "input3": {
            "type": "boolean",
            "tooltip": "Select the third input boolean."
        }
    }