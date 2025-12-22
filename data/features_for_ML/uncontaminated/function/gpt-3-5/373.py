def build_finetune_dataset(
    rag_system: RAGSystem,
    examples: Sequence[dict],
    eos_token_id: int,
    finetune_example_template: str = DEFAULT_FINETUNE_EXAMPLE_TEMPLATE,
    query_key: str = "query",
    answer_key: str = "answer",
    return_dataset: ReturnType = ReturnType.PYTORCH,
) -> Any:
    dataset = []
    for example in examples:
        query = example.get(query_key, "")
        answer = example.get(answer_key, "")
        finetune_example = finetune_example_template.format(query=query, answer=answer)
        input_ids = rag_system.tokenizer.encode(finetune_example, return_tensors="pt")
        dataset.append((input_ids, torch.tensor([eos_token_id])))
    
    if return_dataset == ReturnType.PYTORCH:
        return dataset
    elif return_dataset == ReturnType.TENSORFLOW:
        return [(input_ids.numpy(), np.array([eos_token_id])) for input_ids, _ in dataset]
    else:
        raise ValueError("Invalid return_dataset type")