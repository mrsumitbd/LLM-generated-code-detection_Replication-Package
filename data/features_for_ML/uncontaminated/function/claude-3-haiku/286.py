def feat_training_for_one_split(
    split: str,
    use_corpus: bool,
    use_matrix_input: bool,
    use_pretrained_model: bool,
    cfg,
    verbose=True,
):
    from transformers import AutoTokenizer, AutoModel
    import torch
    from torch.utils.data import DataLoader
    from tqdm import tqdm

    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    model = AutoModel.from_pretrained(cfg.model_name)

    # Load the dataset for the given split
    dataset = load_dataset(split, cfg, use_corpus, use_matrix_input)
    dataloader = DataLoader(dataset, batch_size=cfg.batch_size, shuffle=True)

    # Fine-tune the model
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    for epoch in range(cfg.num_epochs):
        epoch_loss = 0
        for batch in tqdm(dataloader, desc=f"Epoch {epoch+1}/{cfg.num_epochs}", disable=not verbose):
            optimizer.zero_grad()
            output = model(**batch)
            loss = output.loss
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        if verbose:
            print(f"Epoch {epoch+1}/{cfg.num_epochs}, Loss: {epoch_loss/len(dataloader):.4f}")

    # Save the fine-tuned model
    model.save_pretrained(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)