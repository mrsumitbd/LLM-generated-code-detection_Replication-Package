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
    
    return model_spec, system_message, tokenizer, pixel_values, question, history, num_patches_list, IMG_START_TOKEN, IMG_END_TOKEN, IMG_CONTEXT_TOKEN, llm_only