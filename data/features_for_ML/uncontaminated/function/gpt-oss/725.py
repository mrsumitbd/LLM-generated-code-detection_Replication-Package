import os
import json
import logging
from typing import Any

try:
    import openai
except ImportError:
    openai = None

logger = logging.getLogger(__name__)

def call_llm(prompt: str) -> str:
    """
    Send a prompt to an LLM (OpenAI by default) and return the response text.

    Parameters
    ----------
    prompt : str
        The prompt to send to the LLM.

    Returns
    -------
    str
        The LLM's response text.

    Raises
    ------
    RuntimeError
        If the OpenAI library is not available or the API key is missing.
    """
    if openai is None:
        raise RuntimeError("The 'openai' package is required to call an LLM.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
            n=1,
            stop=None,
        )
        content = response.choices[0].message.content.strip()
        return content
    except Exception as exc:
        logger.exception("Failed to call LLM: %s", exc)
        raise RuntimeError(f"LLM call failed: {exc}") from exc