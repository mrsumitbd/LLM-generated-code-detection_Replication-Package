def __rollout(
    model: GenerationMixin,
    tokenizer: PreTrainedTokenizer,
    prompt: Sequence[str],
    device: str = "cpu",
) -> Sequence[str]:
    model.to(device)
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=50)
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return [output_text]