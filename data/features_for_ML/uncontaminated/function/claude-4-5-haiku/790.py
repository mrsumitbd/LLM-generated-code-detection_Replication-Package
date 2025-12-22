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
    
    import base64
    from io import BytesIO
    
    def encode_image(img: Image.Image) -> str:
        """Encode PIL Image to base64 string"""
        if img is None:
            return None
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")
    
    # Build the message content
    content = []
    
    # Add text prompt
    prompt_text = f"Goal: {goal}\n\n"
    
    if generated_steps:
        prompt_text += "Previous steps:\n"
        for i, step in enumerate(generated_steps, 1):
            prompt_text += f"{i}. {step.get('action', '')}\n"
        prompt_text += "\n"
    
    prompt_text += f"Current step: {current_step_value.get('action', '')}\n"
    prompt_text += "Please analyze this step and provide chain-of-thought reasoning.\n"
    
    if need_double_check:
        prompt_text += "Double-check the validity of this step.\n"
    
    if with_prior_judge:
        prompt_text += "Consider prior judgments and consistency.\n"
    
    if not skip_reflection:
        prompt_text += "Provide reflection on the step's effectiveness.\n"
    
    content.append({
        "type": "text",
        "text": prompt_text
    })
    
    # Add images
    if image is not None:
        image_b64 = encode_image(image)
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_b64
            }
        })
    
    if image_patch is not None:
        patch_b64 = encode_image(image_patch)
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": patch_b64
            }
        })
    
    if next_image is not None:
        next_b64 = encode_image(next_image)
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": next_b64
            }
        })
    
    # Call the API
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    # Extract response
    response_text = response.content[0].text if response.content else ""
    
    return {
        "reasoning": response_text,
        "step": current_step_value,
        "valid": True,
        "reflection": response_text if not skip_reflection else None
    }