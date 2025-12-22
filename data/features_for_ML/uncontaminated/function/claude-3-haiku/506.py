from rich.console import Console
from rich.table import Table

def log_mismatch(
    question_id: str,
    question: str,
    model_output: str,
    gold_sql: str,
    prediction_results: Any,
    gold_results: Any,
) -> None:
    """Pretty-print a mismatch with Rich."""
    console = Console()
    table = Table(show_header=False, show_edge=False, padding=(0, 1))

    table.add_row("Question ID:", question_id)
    table.add_row("Question:", question)
    table.add_row("Model Output:", model_output)
    table.add_row("Gold SQL:", gold_sql)
    table.add_row("Prediction Results:", str(prediction_results))
    table.add_row("Gold Results:", str(gold_results))

    console.print(table)