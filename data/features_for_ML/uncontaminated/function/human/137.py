from typing import Annotated

def avatar_tool(
    description: Annotated[str, "Description of the AI avatar, including features, style, and personality."],
):
    """Generates an avatar/image for an AI agent. Creates a suitable AI image based on the provided description."""
    logger.info(f"Generating AI avatar, description: {description}")
    try:
        # Format the prompt
        formatted_prompt = avatar_prompt.format(description=description)
        
        # Call _call to generate the image
        _call(formatted_prompt)
        
        return "AI avatar generated successfully. Please check the image file in the current directory."
    except Exception as e:
        # Catch any exceptions
        error_message = f"Error generating AI avatar: {str(e)}"
        logger.error(error_message)
        return error_message