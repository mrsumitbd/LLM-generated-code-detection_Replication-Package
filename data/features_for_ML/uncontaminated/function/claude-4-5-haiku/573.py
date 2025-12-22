def prepare_model_for_training(model: "PreTrainedModel", model_args: "ModelArguments") -> None:
    r"""
    Includes:
        (1) cast the layernorm in fp32
        (2) make output embedding layer require grads
        (3) add the upcasting of the lm_head in fp32
    """
    if model_args.fp16:
        # (1) cast the layernorm in fp32
        for name, module in model.named_modules():
            if "norm" in name.lower():
                module.to(torch.float32)
        
        # (2) make output embedding layer require grads
        if hasattr(model, "get_output_embeddings"):
            output_embeddings = model.get_output_embeddings()
            if output_embeddings is not None:
                output_embeddings.weight.requires_grad_(True)
        
        # (3) add the upcasting of the lm_head in fp32
        if hasattr(model, "lm_head"):
            model.lm_head.to(torch.float32)