def save_pretrained(args: CkptConverterConfig):
    """
    Saves the converted PyTorch model checkpoint to the specified output directory.

    Args:
        args (CkptConverterConfig): A dataclass containing the configuration for the checkpoint conversion process.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load the PyTorch model
    model = load_model(args.model_path, args.device)

    # Convert the model to the desired format (e.g., ONNX, TensorFlow)
    converted_model = convert_model(model, args.output_format, args.input_size)

    # Save the converted model to the output directory
    save_model(converted_model, args.output_dir, args.output_format)

    # Save the model configuration (if applicable)
    if args.save_config:
        save_config(args, os.path.join(args.output_dir, 'config.json'))

    # Log the successful conversion
    logger.info(f"Model successfully converted and saved to {args.output_dir}")