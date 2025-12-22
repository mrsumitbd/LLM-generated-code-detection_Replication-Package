import logging

class ReActorOptions:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "input_faces_order": ("STRING", {"default": ""}),
            "input_faces_index": ("STRING", {"default": ""}),
            "detect_gender_input": ("BOOLEAN", {"default": False}),
            "source_faces_order": ("STRING", {"default": ""}),
            "source_faces_index": ("STRING", {"default": ""}),
            "detect_gender_source": ("BOOLEAN", {"default": False}),
            "console_log_level": ("STRING", {"default": "INFO"}),
            "restore_swapped_only": ("BOOLEAN", {"default": False}),
        }

    def _parse_list(self, value: str):
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    def _parse_int_list(self, value: str):
        result = []
        for item in self._parse_list(value):
            try:
                result.append(int(item))
            except ValueError:
                result.append(item)
        return result

    def _log_level(self, level_str: str):
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return level_map.get(level_str.upper(), logging.INFO)

    def execute(
        self,
        input_faces_order,
        input_faces_index,
        detect_gender_input,
        source_faces_order,
        source_faces_index,
        detect_gender_source,
        console_log_level,
        restore_swapped_only,
    ):
        options = {
            "input_faces_order": self._parse_list(input_faces_order),
            "input_faces_index": self._parse_int_list(input_faces_index),
            "detect_gender_input": bool(detect_gender_input),
            "source_faces_order": self._parse_list(source_faces_order),
            "source_faces_index": self._parse_int_list(source_faces_index),
            "detect_gender_source": bool(detect_gender_source),
            "console_log_level": self._log_level(console_log_level),
            "restore_swapped_only": bool(restore_swapped_only),
        }
        return {"options": options}