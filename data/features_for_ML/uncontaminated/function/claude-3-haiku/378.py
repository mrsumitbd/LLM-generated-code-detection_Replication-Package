def collate_fn(examples):
    input_ids = [example['input_ids'] for example in examples]
    attention_mask = [example['attention_mask'] for example in examples]
    labels = [example['labels'] for example in examples]

    input_ids = torch.tensor(input_ids, dtype=torch.long)
    attention_mask = torch.tensor(attention_mask, dtype=torch.long)
    labels = torch.tensor(labels, dtype=torch.long)

    return {
        'input_ids': input_ids,
        'attention_mask': attention_mask,
        'labels': labels
    }