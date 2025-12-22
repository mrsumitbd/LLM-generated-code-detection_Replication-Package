class ReActorOptions:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "input_faces_order": list,
            "input_faces_index": list,
            "detect_gender_input": bool,
            "source_faces_order": list,
            "source_faces_index": list,
            "detect_gender_source": bool,
            "console_log_level": str,
            "restore_swapped_only": bool
        }

    def execute(self, input_faces_order, input_faces_index, detect_gender_input, source_faces_order, source_faces_index, detect_gender_source, console_log_level, restore_swapped_only):
        pass