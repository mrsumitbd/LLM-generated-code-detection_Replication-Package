
class ReActorOptions:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_faces_order": (
                    ["left-right","right-left","top-bottom","bottom-top","small-large","large-small"], {"default": "large-small"}
                ),
                "input_faces_index": ("STRING", {"default": "0"}),
                "detect_gender_input": (["no","female","male"], {"default": "no"}),
                "source_faces_order": (
                    ["left-right","right-left","top-bottom","bottom-top","small-large","large-small"], {"default": "large-small"}
                ),
                "source_faces_index": ("STRING", {"default": "0"}),
                "detect_gender_source": (["no","female","male"], {"default": "no"}),
                "console_log_level": ([0, 1, 2], {"default": 1}),
                "restore_swapped_only": ("BOOLEAN", {"default": True, "label_off": "no", "label_on": "yes"})
            }
        }

    RETURN_TYPES = ("OPTIONS",)
    FUNCTION = "execute"
    CATEGORY = "🌌 ReActor"

    def execute(self,input_faces_order, input_faces_index, detect_gender_input, source_faces_order, source_faces_index, detect_gender_source, console_log_level, restore_swapped_only):
        options: dict = {
            "input_faces_order": input_faces_order,
            "input_faces_index": input_faces_index,
            "detect_gender_input": detect_gender_input,
            "source_faces_order": source_faces_order,
            "source_faces_index": source_faces_index,
            "detect_gender_source": detect_gender_source,
            "console_log_level": console_log_level,
            "restore_swapped_only": restore_swapped_only,
        }
        return (options, )