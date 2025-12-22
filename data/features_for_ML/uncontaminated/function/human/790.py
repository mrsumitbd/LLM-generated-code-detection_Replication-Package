from module.reflector import gen_reflection_thought
from module.reflector_with_prior_judge import gen_reflection_thought_with_prior_judge
from utils import (
    load_image, 
    image_to_base64,    
    draw_bounding_box_and_crop_patch,
    call_llm,
    )
from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError
from loguru import logger
import traceback
from PIL import Image
from typing import List
from module.generator import (
    COT_GENERATOR_PROMPT_FOR_MOUSE_ACTION,
    COT_GENERATOR_PROMPT_FOR_KEYBOARD_ACTION,
    REFLECT_COT_GENERATOR_PROMPT_FOR_MOUSE_ACTION,
    REFLECT_COT_GENERATOR_PROMPT_FOR_KEYBOARD_ACTION,
    parse_generator_response,
    DOUBLE_CHECK_PROMPT
)

def generate_cot(
    client, 
    model:str,
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

    try:
        current_action = current_step_value['code']
        if not generated_steps:
            last_step_correct = True
            last_step_redundant = False
            former_thought = "None"
            former_action_effect = "None"
        else:
            last_step_correct = generated_steps[-1]['value']['last_step_correct']
            last_step_redundant = generated_steps[-1]['value'].get('last_step_redundant', False)
            former_thought = generated_steps[-1]['value']['thought']
            former_action_effect = generated_steps[-1]['value']['reflection']

        history_steps = generate_all_history(generated_steps)

        if last_step_correct and not last_step_redundant:
            if image_patch is None:
                prompt = COT_GENERATOR_PROMPT_FOR_KEYBOARD_ACTION
            else:
                prompt = COT_GENERATOR_PROMPT_FOR_MOUSE_ACTION
        else:
            if image_patch is None:
                prompt = REFLECT_COT_GENERATOR_PROMPT_FOR_KEYBOARD_ACTION
            else:
                prompt = REFLECT_COT_GENERATOR_PROMPT_FOR_MOUSE_ACTION

        prompt = prompt.format(
            goal=goal, 
            previous_actions=history_steps,
            former_thought=former_thought,
            former_action_effect=former_action_effect,
            action_commands=current_action
            )

        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_to_base64(image)}", "detail": "high"}}
        ]
        if image_patch is not None:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_to_base64(image_patch)}", "detail": "high"}})
        
        messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ]
        response = call_llm(client, messages, model=model)

        logger.info(f"Generator response: {response}")

        if need_double_check:
            messages=[
                    {
                        "role": "user",
                        "content": content,
                    },
                    {
                        "role": "assistant",
                        "content": response, 
                    },
                    {
                        "role": "user",
                        "content": {"type": "text", "text": DOUBLE_CHECK_PROMPT}, 
                    }
                ]
            response = call_llm(client, messages, model=model)
            logger.info(f"Double Check Response: {response}")

        current_step = current_step_value.copy()
        current_step.update(parse_generator_response(response))
        current_step['code'] = current_action

        if not skip_reflection:
            if with_prior_judge:
                reflect_response = gen_reflection_thought_with_prior_judge(
                    client, 
                    model=model,
                    goal=goal,
                    history_steps=history_steps,
                    current_step=current_step,
                    image=image,
                    image_patch=image_patch,
                    next_image=next_image,
                    )
            else:
                reflect_response = gen_reflection_thought(
                    client, 
                    model=model,
                    goal=goal,
                    history_steps=history_steps,
                    current_step=current_step,
                    image=image,
                    image_patch=image_patch,
                    next_image=next_image,
                    )

            if with_prior_judge:
                current_step['last_step_redundant'] = not current_step['last_step_correct']
                current_step['reflection'] = reflect_response['reflection']
            else:
                current_step['last_step_correct'] = reflect_response['last_step_correct']
                current_step['last_step_redundant'] = reflect_response['last_step_redundant']
                current_step['reflection'] = reflect_response['reflection']
        else:
            current_step['last_step_correct'] = True
            current_step['last_step_redundant'] = False
            current_step['reflection'] = ""
            
        return current_step
    
    except (APITimeoutError, APIConnectionError, RateLimitError) as e:
        print("=" * 100)
        print(f"API Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"Retrying... (controlled by backoff decorator)")
        print("=" * 100)
        raise  

    except Exception as e:
        print("=" * 100)
        print(f"Unexpected Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        print("=" * 100)
        raise