from typing import Any
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
    table = Table(
        title=f"[red]Mismatch for Question {question_id}[/red]", show_lines=True
    )
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", overflow="fold")

    table.add_row("Question", question)
    table.add_row("Model Output SQL", model_output.strip())
    table.add_row("Gold SQL", gold_sql.strip())
    table.add_row("Prediction Results", str(prediction_results))
    table.add_row("Gold Results", str(gold_results))

    console.print(table)