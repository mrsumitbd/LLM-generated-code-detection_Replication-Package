def prepare(
    model_spec,
    system_message,
    tokenizer,
    pixel_values,
    question,
    history=None,
    num_patches_list=None,
    IMG_START_TOKEN='<img>',
    IMG_END_TOKEN='</img>',
    IMG_CONTEXT_TOKEN='<IMG_CONTEXT>',
    llm_only=False,
):
    if history is None:
        history = []

    if num_patches_list is None:
        num_patches_list = []

    if llm_only:
        return {
            "system_message": system_message,
            "messages": [{"role": "user", "content": question}],
            "history": history,
        }

    image_tokens = []
    for i, patch in enumerate(pixel_values):
        image_tokens.append(IMG_START_TOKEN)
        image_tokens.extend(tokenizer.encode(str(i)))
        image_tokens.append(IMG_END_TOKEN)
        if i < len(pixel_values) - 1:
            image_tokens.append(IMG_CONTEXT_TOKEN)

    if model_spec == "llm_and_vision":
        return {
            "system_message": system_message,
            "messages": [
                {"role": "user", "content": " ".join(image_tokens) + " " + question},
            ],
            "history": history,
            "num_patches_list": num_patches_list,
        }
    elif model_spec == "vision_only":
        return {
            "pixel_values": pixel_values,
            "num_patches_list": num_patches_list,
        }
    elif model_spec == "llm_only":
        return {
            "system_message": system_message,
            "messages": [{"role": "user", "content": question}],
            "history": history,
        }
    else:
        raise ValueError(f"Invalid model_spec: {model_spec}")