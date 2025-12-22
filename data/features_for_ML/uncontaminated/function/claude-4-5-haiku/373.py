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
    
    processed_examples = []
    
    for example in examples:
        query = example.get(query_key, "")
        answer = example.get(answer_key, "")
        
        # Retrieve context using RAG system
        retrieved_docs = rag_system.retrieve(query)
        context = "\n".join([doc.get("content", "") for doc in retrieved_docs]) if retrieved_docs else ""
        
        # Format the example using the template
        formatted_example = finetune_example_template.format(
            query=query,
            context=context,
            answer=answer
        )
        
        # Tokenize the formatted example
        tokens = rag_system.tokenizer.encode(formatted_example)
        tokens.append(eos_token_id)
        
        processed_examples.append({
            "input_ids": tokens,
            "attention_mask": [1] * len(tokens),
        })
    
    # Convert to appropriate dataset format
    if return_dataset == ReturnType.PYTORCH:
        import torch
        from torch.utils.data import Dataset
        
        class FinetuneDataset(Dataset):
            def __init__(self, examples):
                self.examples = examples
            
            def __len__(self):
                return len(self.examples)
            
            def __getitem__(self, idx):
                example = self.examples[idx]
                return {
                    "input_ids": torch.tensor(example["input_ids"], dtype=torch.long),
                    "attention_mask": torch.tensor(example["attention_mask"], dtype=torch.long),
                }
        
        return FinetuneDataset(processed_examples)
    
    elif return_dataset == ReturnType.HUGGINGFACE:
        from datasets import Dataset
        return Dataset.from_dict({
            "input_ids": [ex["input_ids"] for ex in processed_examples],
            "attention_mask": [ex["attention_mask"] for ex in processed_examples],
        })
    
    else:
        return processed_examples