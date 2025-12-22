def evaluate(
    ctx: typer.Context,
    task: Annotated[
        str,
        typer.Option(
            ...,
            help="Task to process.",
            click_type=click.Choice(list(TASK_NAMES_TO_YAML.keys())),
            case_sensitive=False,
        ),
    ],
    model: Annotated[str, typer.Option(..., help="The model to run")],
    backend: Annotated[
        Backend,
        typer.Option(
            help="Backend to use for inference.",
            case_sensitive=False,
        ),
    ] = Backend.VLLM,
    backend_args: Annotated[
        str,
        typer.Option(
            help="Backend parameters to use for inference.",
            case_sensitive=False,
        ),
    ] = "",
    sampling_params: Annotated[
        str,
        typer.Option(
            help="Sampling parameters to use for inference.",
            case_sensitive=False,
        ),
    ] = SAMPLING_PARAMS_DEFAULT,
    result_dir: Annotated[
        str,
        typer.Option(
            help="Result directory to save outputs.",
        ),
    ] = "./",
    system_prompt_name: Annotated[
        str,
        typer.Option(
            help="System prompt template to use, overriding any pre-configured system prompt for this model.",
            click_type=click.Choice(get_system_prompt_keys()),
        ),
    ] = None,
    system_prompt: Annotated[
        str,
        typer.Option(
            help="System prompt to use, overriding any pre-configured system prompt for this model."
        ),
    ] = None,
    n: Annotated[
        int, typer.Option(help="Number of samples generated per problem.")
    ] = None,
    seed: Annotated[int, typer.Option(help="Random seed.")] = 41,
    assistant_prefill: Annotated[
        str,
        typer.Option(
            help=r'Assistant prefill for the model response, overriding any pre-configured assistant prefill for this model. Ex: "<think>\n"'
        ),
    ] = None,
    as_test: Annotated[
        bool, typer.Option(help="Perform a test run on 10 samples of the dataset.")
    ] = False,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing results.")
    ] = False,
    batch_size: Annotated[
        int,
        typer.Option(
            help="Batch size for inference. only applicable for the vllm backend."
        ),
    ] = 64,
):
    import json
    from pathlib import Path
    
    # Create result directory
    result_path = Path(result_dir)
    result_path.mkdir(parents=True, exist_ok=True)
    
    # Load task configuration
    task_yaml_path = TASK_NAMES_TO_YAML.get(task.lower())
    if not task_yaml_path:
        typer.echo(f"Error: Task '{task}' not found.", err=True)
        raise typer.Exit(code=1)
    
    # Parse backend arguments
    backend_kwargs = {}
    if backend_args:
        try:
            backend_kwargs = json.loads(backend_args)
        except json.JSONDecodeError:
            typer.echo(f"Error: Invalid backend arguments JSON: {backend_args}", err=True)
            raise typer.Exit(code=1)
    
    # Parse sampling parameters
    sampling_kwargs = {}
    if sampling_params:
        try:
            sampling_kwargs = json.loads(sampling_params)
        except json.JSONDecodeError:
            typer.echo(f"Error: Invalid sampling parameters JSON: {sampling_params}", err=True)
            raise typer.Exit(code=1)
    
    # Determine system prompt
    final_system_prompt = None
    if system_prompt:
        final_system_prompt = system_prompt
    elif system_prompt_name:
        final_system_prompt = get_system_prompt(system_prompt_name)
    
    # Create inference configuration
    inference_config = {
        "model": model,
        "backend": backend,
        "backend_args": backend_kwargs,
        "sampling_params": sampling_kwargs,
        "batch_size": batch_size,
        "seed": seed,
        "system_prompt": final_system_prompt,
        "assistant_prefill": assistant_prefill,
        "n": n,
    }
    
    # Load dataset
    dataset = load_task_dataset(task_yaml_path, as_test=as_test)
    
    # Check if results already exist
    result_file = result_path / f"{task}_{model}_results.jsonl"
    if result_file.exists() and not overwrite:
        typer.echo(f"Results already exist at {result_file}. Use --overwrite to replace.", err=True)
        raise typer.Exit(code=1)
    
    # Run inference
    results = run_inference(
        dataset=dataset,
        config=inference_config,
    )
    
    # Save results
    with open(result_file, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    
    typer.echo(f"Results saved to {result_file}")