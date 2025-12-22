import os
from ..utils import folder_paths, get_filename_list, get_full_path_or_raise

def INPUT_TYPES(s):
        """
        Defines the input types and tooltips for the node.

        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        """
        prefixes = folder_paths.folder_names_and_paths["text_encoders"][0]
        local_folders = set()
        for prefix in prefixes:
            if os.path.exists(prefix) and os.path.isdir(prefix):
                local_folders_ = os.listdir(prefix)
                local_folders_ = [
                    folder
                    for folder in local_folders_
                    if not folder.startswith(".") and os.path.isdir(os.path.join(prefix, folder))
                ]
                local_folders.update(local_folders_)
        model_paths = ["none"] + sorted(list(local_folders))
        return {
            "required": {
                "model_type": (["flux"],),
                "text_encoder1": (get_filename_list("text_encoders"),),
                "text_encoder2": (get_filename_list("text_encoders"),),
                "t5_min_length": (
                    "INT",
                    {
                        "default": 512,
                        "min": 256,
                        "max": 1024,
                        "step": 128,
                        "display": "number",
                        "lazy": True,
                        "tooltip": "Minimum sequence length for the T5 encoder.",
                    },
                ),
                "use_4bit_t5": (["disable", "enable"],),
                "int4_model": (
                    model_paths,
                    {"tooltip": "The name of the 4-bit T5 model."},
                ),
            }
        }