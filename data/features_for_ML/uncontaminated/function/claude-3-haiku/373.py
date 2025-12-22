def build_finetune_dataset(
    rag_system: RAGSystem,
    examples: Sequence[dict],
    eos_token_id: int,
    finetune_example_template: str = DEFAULT_FINETUNE_EXAMPLE_TEMPLATE,
    query_key: str = "query",
    answer_key: str = "answer",
    return_dataset: ReturnType = ReturnType.PYTORCH,
) -> Any:
    """Generates the finetuning dataset using the supplied rag_system and examples."""
    input_ids = []
    attention_masks = []
    labels = []

    for example in examples:
        query = example[query_key]
        answer = example[answer_key]

        input_id, attention_mask = rag_system.encode(query, finetune_example_template)
        label_id = rag_system.encode(answer, finetune_example_template)[0]

        input_ids.append(input_id)
        attention_masks.append(attention_mask)
        labels.append(label_id)

    if return_dataset == ReturnType.PYTORCH:
        return TensorDataset(
            torch.tensor(input_ids, dtype=torch.long),
            torch.tensor(attention_masks, dtype=torch.long),
            torch.tensor(labels, dtype=torch.long),
        )
    elif return_dataset == ReturnType.TENSORFLOW:
        return tf.data.Dataset.from_tensor_slices((
            {"input_ids": input_ids, "attention_mask": attention_masks},
            labels
        ))
    else:
        raise ValueError(f"Unsupported return_dataset type: {return_dataset}")