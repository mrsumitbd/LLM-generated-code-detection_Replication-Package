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
    
    # Build the conversation history
    messages = []
    
    # Add system message
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # Add history
    for hist_item in history:
        if isinstance(hist_item, dict):
            messages.append(hist_item)
        elif isinstance(hist_item, tuple) and len(hist_item) == 2:
            messages.append({"role": "user", "content": hist_item[0]})
            messages.append({"role": "assistant", "content": hist_item[1]})
    
    # Add current question with image tokens
    if pixel_values is not None and len(pixel_values) > 0:
        # Construct message with image tokens
        image_token_str = ""
        for i, num_patches in enumerate(num_patches_list):
            image_token_str += IMG_START_TOKEN
            image_token_str += IMG_CONTEXT_TOKEN * num_patches
            image_token_str += IMG_END_TOKEN
        
        content = image_token_str + "\n" + question if image_token_str else question
    else:
        content = question
    
    messages.append({"role": "user", "content": content})
    
    # Tokenize the messages
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # Tokenize to get input_ids
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )
    
    input_ids = inputs["input_ids"]
    attention_mask = inputs.get("attention_mask", None)
    
    # Prepare output dictionary
    output = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "pixel_values": pixel_values,
    }
    
    if num_patches_list:
        output["num_patches_list"] = num_patches_list
    
    return output