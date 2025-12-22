def __rollout(
        model: GenerationMixin,
        tokenizer: PreTrainedTokenizer,
        prompt: Sequence[str],
        device: str = "cpu",
    ) -> Sequence[str]:
    
    # Move the model to the specified device
    model.to(device)
    
    # Generate the output sequences
    output_sequences = model.generate(
        input_ids=tokenizer(prompt, return_tensors="pt").input_ids.to(device),
        max_length=model.config.max_length,
        num_return_sequences=len(prompt),
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_beams=1,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=1.0,
        no_repeat_ngram_size=3,
    )
    
    # Decode the output sequences
    output_text = [tokenizer.decode(seq, skip_special_tokens=True) for seq in output_sequences]
    
    return output_text