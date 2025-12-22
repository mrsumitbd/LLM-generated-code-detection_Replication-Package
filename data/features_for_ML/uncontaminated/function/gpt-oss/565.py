import os
from typing import Any

# Try to import the Gemini library; raise a clear error if unavailable.
try:
    import google.generativeai as genai
except Exception as exc:
    raise ImportError(
        "The 'google.generativeai' package is required to use get_model. "
        "Install it with `pip install google-generativeai`."
    ) from exc

# Default model name if not provided elsewhere.
GEMINI_PRO: str = "gemini-pro"

def get_model(
    name: str = GEMINI_PRO,
    temperature: float = 0.2,
    top_p: float = 0.95,
    top_k: int = 40,
    max_output_tokens: int = 2048,
) -> Any:
    """
    Create and return a Gemini GenerativeModel instance with the specified
    configuration.

    Parameters
    ----------
    name : str, optional
        The name of the Gemini model to instantiate. Defaults to GEMINI_PRO.
    temperature : float, optional
        Controls randomness in generation. Defaults to 0.2.
    top_p : float, optional
        Nucleus sampling parameter. Defaults to 0.95.
    top_k : int, optional
        Top-k sampling parameter. Defaults to 40.
    max_output_tokens : int, optional
        Maximum number of tokens in the generated response. Defaults to 2048.

    Returns
    -------
    Any
        An instance of `google.generativeai.GenerativeModel` configured with
        the provided parameters.
    """
    # Ensure the API key is configured if not already done.
    if not getattr(genai, "configured", False):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Set it to your Gemini API key before calling get_model."
            )
        genai.configure(api_key=api_key)

    # Instantiate and return the model.
    return genai.GenerativeModel(
        name=name,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        max_output_tokens=max_output_tokens,
    )