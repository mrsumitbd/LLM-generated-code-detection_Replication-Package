def feat_training_for_one_split(
    split: str,
    use_corpus: bool,
    use_matrix_input: bool,
    use_pretrained_model: bool,
    cfg,
    verbose=True,
):
    if verbose:
        print(f"Training features for split: {split}")
        print(f"Use Corpus: {use_corpus}")
        print(f"Use Matrix Input: {use_matrix_input}")
        print(f"Use Pretrained Model: {use_pretrained_model}")
        print(f"Config: {cfg}")
    # Add your feature training code here
    # Return any relevant output if needed