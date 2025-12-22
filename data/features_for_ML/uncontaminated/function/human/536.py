from internmanip.model.backbone.eagle2_hg_model.conversation_repo import get_conv_template

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
    if history is None and pixel_values is not None and '<image>' not in question:
        question = '<image>\n' + question

    if num_patches_list is None:
        num_patches_list = [1] * pixel_values.shape[0] if pixel_values is not None else []
    assert pixel_values is None or len(pixel_values) == sum(num_patches_list)

    template = get_conv_template(model_spec.template)
    template.system_message = system_message

    history = [] if history is None else history
    for old_question, old_answer in history:
        template.append_message(template.roles[0], old_question)
        template.append_message(template.roles[1], old_answer)
    template.append_message(template.roles[0], question)
    template.append_message(template.roles[1], None)
    query = template.get_prompt()

    for num_patches in num_patches_list:
        image_tokens = (
            IMG_START_TOKEN
            + IMG_CONTEXT_TOKEN * model_spec.num_image_token * num_patches
            + IMG_END_TOKEN
        )
        if llm_only:
            query = query.replace('<image>', '', 1)
        else:
            query = query.replace('<image>', image_tokens, 1)

    model_inputs = tokenizer(query, return_tensors='pt')

    return (
        pixel_values,
        model_inputs['input_ids'],
        model_inputs['attention_mask'],
    )