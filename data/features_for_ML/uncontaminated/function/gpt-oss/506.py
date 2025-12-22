from typing import Any
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel
import json

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

    # Helper to format results
    def format_result(result: Any) -> str:
        if isinstance(result, (dict, list)):
            return json.dumps(result, indent=2, sort_keys=True)
        return str(result)

    # Syntax highlighting for SQL
    sql_syntax = Syntax(gold_sql, "sql", theme="monokai", line_numbers=True)

    # Build the table
    table = Table.grid(padding=(0, 1))
    table.add_column(justify="right", style="bold cyan")
    table.add_column(justify="left", style="white")

    table.add_row("Question ID:", question_id)
    table.add_row("Question:", question)
    table.add_row("Model Output:", model_output)
    table.add_row("Gold SQL:", sql_syntax)
    table.add_row("Prediction Results:", format_result(prediction_results))
    table.add_row("Gold Results:", format_result(gold_results))

    panel = Panel(
        table,
        title=f"[red]Mismatch for Question {question_id}[/red]",
        border_style="red",
        expand=False,
    )

    console.print(panel)