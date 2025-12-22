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
    
    # Implement the function logic here
    result = {
        "result": "success",
        "next_step": {
            "action": "some_action",
            "value": "some_value"
        }
    }
    
    return result