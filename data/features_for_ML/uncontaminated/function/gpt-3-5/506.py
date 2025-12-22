def log_mismatch(
    question_id: str,
    question: str,
    model_output: str,
    gold_sql: str,
    prediction_results: Any,
    gold_results: Any,
) -> None:
    """Pretty-print a mismatch with Rich."""
    
    from rich import print

    print(f"[bold red]Question ID:[/bold red] {question_id}")
    print(f"[bold blue]Question:[/bold blue] {question}")
    print(f"[bold green]Model Output:[/bold green] {model_output}")
    print(f"[bold yellow]Gold SQL:[/bold yellow] {gold_sql}")
    print(f"[bold cyan]Prediction Results:[/bold cyan] {prediction_results}")
    print(f"[bold magenta]Gold Results:[/bold magenta] {gold_results}")