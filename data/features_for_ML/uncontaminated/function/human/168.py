import asyncio
import typer

def generate(
    task: str = typer.Argument(
        ...,
        help="The task description to generate a program for (e.g., 'Add 5 and 7 and print the result')"
    ),
    model: str = typer.Option(
        "gemini/gemini-2.0-flash",
        "--model",
        "-m",
        help="The litellm model to use for generation (e.g., 'gpt-3.5-turbo', 'gpt-4')"
    ),
    max_tokens: int = typer.Option(
        4000,
        "--max-tokens",
        "-t",
        help="Maximum number of tokens for the generated response (default: 4000)"
    )
):
    """
    Asynchronously generate a Python program based on a task description using specified tools and model.
    Executes the program in a controlled, safe environment.

    Examples:
        $ python action_gen_safe.py "Add 5 and 7 and print the result"
        $ python action_gen_safe.py "Concatenate 'Hello' and 'World' and print it" --model gpt-4 --max-tokens 5000
    """
    asyncio.run(generate_core(task, model, max_tokens))