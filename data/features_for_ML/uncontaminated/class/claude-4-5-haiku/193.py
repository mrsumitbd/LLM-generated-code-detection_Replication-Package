import anthropic
import json
import logging
from typing import Any

class ReActorOptions:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_faces_order": (["top-to-bottom", "bottom-to-top", "left-to-right", "right-to-left", "small-to-large", "large-to-small"],),
                "input_faces_index": ("STRING", {"default": "0"}),
                "detect_gender_input": (["no", "yes"],),
                "source_faces_order": (["top-to-bottom", "bottom-to-top", "left-to-right", "right-to-left", "small-to-large", "large-to-small"],),
                "source_faces_index": ("STRING", {"default": "0"}),
                "detect_gender_source": (["no", "yes"],),
                "console_log_level": (["debug", "info", "warning", "error"],),
                "restore_swapped_only": (["yes", "no"],),
            }
        }

    def execute(self, input_faces_order, input_faces_index, detect_gender_input, source_faces_order, source_faces_index, detect_gender_source, console_log_level, restore_swapped_only):
        # Set up logging based on console_log_level
        log_level = getattr(logging, console_log_level.upper())
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(__name__)
        
        # Create the configuration dictionary
        config = {
            "input_faces_order": input_faces_order,
            "input_faces_index": input_faces_index,
            "detect_gender_input": detect_gender_input == "yes",
            "source_faces_order": source_faces_order,
            "source_faces_index": source_faces_index,
            "detect_gender_source": detect_gender_source == "yes",
            "restore_swapped_only": restore_swapped_only == "yes",
        }
        
        logger.debug(f"ReActorOptions configuration: {json.dumps(config, indent=2)}")
        
        # Use Claude to validate and provide insights about the configuration
        client = anthropic.Anthropic()
        
        prompt = f"""Analyze this ReActor face swap configuration and provide validation feedback:

Configuration:
- Input faces order: {input_faces_order}
- Input faces index: {input_faces_index}
- Detect gender in input: {detect_gender_input}
- Source faces order: {source_faces_order}
- Source faces index: {source_faces_index}
- Detect gender in source: {detect_gender_source}
- Restore swapped only: {restore_swapped_only}

Please provide:
1. Whether this configuration is valid
2. Any potential issues or recommendations
3. What this configuration will do in simple terms"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = message.content[0].text
        logger.info(f"Configuration analysis:\n{analysis}")
        
        return (config,)