import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import request_models

def get_default_video_prompt(
    scene_segments: list[request_models.SceneSegmentRequest],
):
  """
  Retrieves a default template for video generation prompts.

  Args:
      scene_segments: A list of `SceneSegmentRequest` objects (currently
                      unused in this implementation).

  Returns:
      An empty string as a placeholder for a default video prompt.

  Raises:
      HTTPException (500): If an unexpected error occurs.
  """
  try:
    # TODO: Implement actual default video prompt generation logic here.
    return ""
  except Exception as ex:
    logging.error(
        "Dreamboard - VIDEO_GEN_ROUTES-get_default_video_prompt: - ERROR: %s",
        str(ex),
    )
    if os.getenv("USE_AUTH_MIDDLEWARE"):
      error_response = {
          "status_code": 500,
          "error_message": str(ex),
      }
      # Workaround to send the actual error message to NodeJS middleware request handler
      return JSONResponse(content=error_response)
    else:
      raise HTTPException(status_code=500, detail=str(ex)) from ex