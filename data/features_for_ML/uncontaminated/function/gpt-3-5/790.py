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
    
    # Implementation goes here
    result = {
        'client': client,
        'model': model,
        'goal': goal,
        'generated_steps': generated_steps,
        'current_step_value': current_step_value,
        'image': image,
        'image_patch': image_patch,
        'next_image': next_image,
        'need_double_check': need_double_check,
        'with_prior_judge': with_prior_judge,
        'skip_reflection': skip_reflection
    }
    
    return result