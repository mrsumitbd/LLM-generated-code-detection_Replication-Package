def __rollout(
        model: GenerationMixin,
        tokenizer: PreTrainedTokenizer,
        prompt: Sequence[str],
        device: str = "cpu",
    ) -> Sequence[str]:
    model.eval()
    
    with torch.no_grad():
        inputs = tokenizer(
            list(prompt),
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        outputs = model.generate(
            **inputs,
            max_length=512,
            num_return_sequences=1,
            do_sample=False,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )
        
        generated_texts = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
    
    return generated_texts