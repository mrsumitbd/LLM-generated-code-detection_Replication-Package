def prepare_model_for_training(model: "PreTrainedModel", model_args: "ModelArguments") -> None:
    r"""
    Includes:
        (1) cast the layernorm in fp32
        (2) make output embedding layer require grads
        (3) add the upcasting of the lm_head in fp32
    """
    # (1) Cast the layernorm in fp32
    for module in model.modules():
        if isinstance(module, torch.nn.LayerNorm):
            module.float()

    # (2) Make output embedding layer require grads
    model.get_output_embeddings().weight.requires_grad = True

    # (3) Add the upcasting of the lm_head in fp32
    model.lm_head = torch.nn.Linear(
        model.config.hidden_size,
        model.config.vocab_size,
        bias=model.config.tie_word_embeddings
    )
    model.lm_head.weight = model.get_output_embeddings().weight
    model.lm_head.to(torch.float32)