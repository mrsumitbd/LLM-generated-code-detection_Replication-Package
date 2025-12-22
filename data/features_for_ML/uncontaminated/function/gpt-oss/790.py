from typing import List, Dict, Any
from PIL import Image
import base64
import io

def _image_to_base64(img: Image.Image) -> str:
    """Convert a PIL image to a base64 string."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def generate_cot(
    client,
    model: str,
    goal: str,
    generated_steps: List[dict],
    current_step_value: dict,
    image: Image.Image,
    image_patch: Image.Image = None,
    next_image: Image.Image = None,
    need_double_check: bool = False,
    with_prior_judge: bool = False,
    skip_reflection: bool = False,
) -> dict:
    """
    Generate a chain‑of‑thought (CoT) explanation for the current step of a task.

    Parameters
    ----------
    client : OpenAI client
        The client used to call the LLM.
    model : str
        The name of the model to use.
    goal : str
        The overall goal of the task.
    generated_steps : List[dict]
        A list of previously generated steps.
    current_step_value : dict
        The current step that needs a CoT explanation.
    image : PIL.Image.Image
        The image associated with the current step.
    image_patch : PIL.Image.Image, optional
        A patch of the image that might be relevant.
    next_image : PIL.Image.Image, optional
        The image that will be produced after the current step.
    need_double_check : bool, default False
        If True, the LLM will be asked to double‑check its reasoning.
    with_prior_judge : bool, default False
        If True, the LLM will be asked to consider a prior judge’s feedback.
    skip_reflection : bool, default False
        If True, the LLM will not produce a reflection section.

    Returns
    -------
    dict
        A dictionary containing the generated CoT and, if requested,
        a reflection section.
    """
    # Build the system prompt
    system_prompt = (
        "You are an AI assistant that generates chain‑of‑thought explanations "
        "for image‑based tasks. Follow the instructions carefully."
    )

    # Build the user prompt
    user_prompt = f"Goal: {goal}\n\n"
    user_prompt += "Previous steps:\n"
    for i, step in enumerate(generated_steps, 1):
        user_prompt += f"  Step {i}: {step}\n"
    user_prompt += f"\nCurrent step: {current_step_value}\n"

    # Include image information
    if image:
        img_b64 = _image_to_base64(image)
        user_prompt += f"\nImage (base64): {img_b64}\n"
    if image_patch:
        patch_b64 = _image_to_base64(image_patch)
        user_prompt += f"\nImage patch (base64): {patch_b64}\n"
    if next_image:
        next_b64 = _image_to_base64(next_image)
        user_prompt += f"\nNext image (base64): {next_b64}\n"

    # Add flags
    if need_double_check:
        user_prompt += "\nPlease double‑check your reasoning.\n"
    if with_prior_judge:
        user_prompt += "\nConsider any prior judge feedback.\n"
    if not skip_reflection:
        user_prompt += "\nAfter the chain‑of‑thought, provide a brief reflection on the reasoning.\n"

    # Call the model
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=800,
        )
    except Exception as e:
        # In case of an error, return the error message
        return {"cot": f"Error: {e}", "reflection": ""}

    # Extract content
    content = response.choices[0].message.content.strip()

    # Split into CoT and reflection if reflection was requested
    if not skip_reflection:
        # Assume the reflection starts after a marker "Reflection:" if present
        if "Reflection:" in content:
            cot_part, reflection_part = content.split("Reflection:", 1)
            cot = cot_part.strip()
            reflection = reflection_part.strip()
        else:
            # If no explicit marker, treat entire content as CoT
            cot = content
            reflection = ""
    else:
        cot = content
        reflection = ""

    return {"cot": cot, "reflection": reflection}