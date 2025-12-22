def log_mismatch(
    question_id: str,
    question: str,
    model_output: str,
    gold_sql: str,
    prediction_results: Any,
    gold_results: Any,
) -> None:
    """Pretty-print a mismatch with Rich."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    
    console = Console()
    
    # Create a table for the mismatch details
    table = Table(title=f"Mismatch for Question ID: {question_id}", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan")
    table.add_column("Content", style="green")
    
    table.add_row("Question ID", question_id)
    table.add_row("Question", question)
    
    # Add SQL queries with syntax highlighting
    model_sql_syntax = Syntax(model_output, "sql", theme="monokai", line_numbers=True)
    gold_sql_syntax = Syntax(gold_sql, "sql", theme="monokai", line_numbers=True)
    
    table.add_row("Model Output SQL", model_sql_syntax)
    table.add_row("Gold SQL", gold_sql_syntax)
    
    # Add results
    table.add_row("Prediction Results", str(prediction_results))
    table.add_row("Gold Results", str(gold_results))
    
    console.print(table)
    console.print()