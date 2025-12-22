import subprocess
import sys
import textwrap
import typer
import litellm
from pathlib import Path
from typing import Optional

app = typer.Typer()


def _run_code(code: str, timeout: int = 5) -> str:
    """
    Execute the given Python code in a subprocess with a timeout.
    The subprocess is run with a minimal environment to reduce risk.
    """
    # Write code to a temporary file
    tmp_file = Path("/tmp/generated_code.py")
    tmp_file.write_text(code)

    # Build the command
    cmd = [sys.executable, str(tmp_file)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={"PYTHONPATH": "", "PATH": "/usr/bin:/bin"},
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if result.returncode != 0:
            return f"❌ Execution failed (exit {result.returncode}):\n{stderr}"
        return f"✅ Output:\n{stdout}"
    except subprocess.TimeoutExpired:
        return "❌ Execution timed out."
    finally:
        try:
            tmp_file.unlink()
        except Exception:
            pass


def _generate_code(task: str, model: str, max_tokens: int) -> Optional[str]:
    """
    Call the LLM to generate Python code for the given task.
    """
    system_prompt = (
        "You are a helpful assistant that writes clean, safe Python code. "
        "Respond with only the code, no explanations or comments."
    )
    user_prompt = f"Write a Python program that {task}."

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        # litellm returns a dict with 'choices'
        content = response["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        typer.echo(f"❌ LLM request failed: {e}")
        return None


@app.command()
def generate(
    task: str = typer.Argument(
        ...,
        help="The task description to generate a program for (e.g., 'Add 5 and 7 and print the result')",
    ),
    model: str = typer.Option(
        "gemini/gemini-2.0-flash",
        "--model",
        "-m",
        help="The litellm model to use for generation (e.g., 'gpt-3.5-turbo', 'gpt-4')",
    ),
    max_tokens: int = typer.Option(
        4000,
        "--max-tokens",
        "-t",
        help="Maximum number of tokens for the generated response (default: 4000)",
    ),
):
    """
    Asynchronously generate a Python program based on a task description using specified tools and model.
    Executes the program in a controlled, safe environment.

    Examples:
        $ python action_gen_safe.py "Add 5 and 7 and print the result"
        $ python action_gen_safe.py "Concatenate 'Hello' and 'World' and print it" --model gpt-4 --max-tokens 5000
    """
    typer.echo(f"🔍 Generating code for task: {task}")
    code = _generate_code(task, model, max_tokens)
    if not code:
        typer.echo("❌ No code generated.")
        raise typer.Exit(1)

    typer.echo("\n📝 Generated code:\n")
    typer.echo(textwrap.indent(code, "    "))

    typer.echo("\n🚀 Running the generated code...")
    output = _run_code(code)
    typer.echo("\n" + output)


if __name__ == "__main__":
    app()