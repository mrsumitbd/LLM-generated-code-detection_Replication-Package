import json
import os
from typing import Any, Dict, List, Optional

def _get_executor() -> Any:
    """
    Attempt to retrieve the executor object from the global namespace.
    The executor is expected to provide either:
      - a `get_history()` method returning a list of dicts with keys
        'code', 'output', and optionally 'execution_count'.
      - or attributes `code_blocks` (list of str) and `results` (list of str).
    """
    # Try to import a module named 'executor' if it exists
    try:
        import executor  # type: ignore
        return executor
    except Exception:
        pass

    # Fallback to global variable
    return globals().get("executor", None)


def _format_output(output: str) -> List[Dict[str, Any]]:
    """
    Convert a plain string output into a Jupyter notebook output cell.
    """
    if output is None:
        return []
    # Ensure output ends with a newline for proper display
    if not output.endswith("\n"):
        output += "\n"
    return [
        {
            "output_type": "stream",
            "name": "stdout",
            "text": [output],
        }
    ]


def _build_notebook_cells(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build notebook cells from the conversation history.
    """
    cells = []
    for idx, entry in enumerate(history, start=1):
        code = entry.get("code", "")
        output = entry.get("output", "")
        execution_count = entry.get("execution_count", idx)

        cell = {
            "cell_type": "code",
            "metadata": {},
            "source": [code + ("\n" if not code.endswith("\n") else "")],
            "outputs": _format_output(output),
            "execution_count": execution_count,
        }
        cells.append(cell)
    return cells


def _default_metadata() -> Dict[str, Any]:
    """
    Default notebook metadata.
    """
    return {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11",
        },
    }


def save_conversation_history_to_notebook(file_path: str = "notebook.ipynb") -> None:
    """
    Save the conversation history to an IPython notebook file (.ipynb).

    This function retrieves the code blocks and their execution results from the
    executor, formats them as notebook cells, and saves them to a .ipynb file
    in JSON format.

    Args:
        file_path (str): The path to save the notebook to. Defaults to "notebook.ipynb".

    Raises:
        Exception: If there is an error during notebook creation or file saving.
    """
    try:
        executor = _get_executor()
        if executor is None:
            raise Exception("No executor found in the global namespace.")

        # Retrieve history
        history: Optional[List[Dict[str, Any]]] = None

        if hasattr(executor, "get_history") and callable(executor.get_history):
            history = executor.get_history()
        elif hasattr(executor, "code_blocks") and hasattr(executor, "results"):
            code_blocks = getattr(executor, "code_blocks")
            results = getattr(executor, "results")
            if not isinstance(code_blocks, list) or not isinstance(results, list):
                raise Exception("executor.code_blocks and executor.results must be lists.")
            if len(code_blocks) != len(results):
                raise Exception("executor.code_blocks and executor.results must have the same length.")
            history = [
                {"code": cb, "output": res, "execution_count": idx + 1}
                for idx, (cb, res) in enumerate(zip(code_blocks, results))
            ]
        else:
            raise Exception("Executor does not provide a usable history interface.")

        if not isinstance(history, list):
            raise Exception("History must be a list of dictionaries.")

        # Build notebook cells
        cells = _build_notebook_cells(history)

        # Assemble notebook structure
        notebook = {
            "cells": cells,
            "metadata": _default_metadata(),
            "nbformat": 4,
            "nbformat_minor": 5,
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=2)

    except Exception as exc:
        raise Exception(f"Failed to save notebook: {exc}") from exc