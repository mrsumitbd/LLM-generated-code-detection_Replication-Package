class ReActorOptions:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'input_faces_order': None,
            'input_faces_index': None,
            'detect_gender_input': None,
            'source_faces_order': None,
            'source_faces_index': None,
            'detect_gender_source': None,
            'console_log_level': None,
            'restore_swapped_only': None
        }

    def execute(self, input_faces_order, input_faces_index, detect_gender_input, source_faces_order, source_faces_index, detect_gender_source, console_log_level, restore_swapped_only):
        # Your implementation here
        pass