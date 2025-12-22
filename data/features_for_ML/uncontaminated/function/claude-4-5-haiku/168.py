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
    import asyncio
    import litellm
    import re
    
    async def generate_and_execute():
        system_prompt = """You are a Python code generator. Generate a complete, executable Python program that accomplishes the given task.
        
Requirements:
- Generate only valid Python code
- The code should be self-contained and executable
- Wrap the code in a markdown code block with ```python and ```
- Do not include any explanations outside the code block
- Ensure the code is safe and does not perform harmful operations"""
        
        try:
            response = await asyncio.to_thread(
                litellm.completion,
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Task: {task}"}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            generated_code = response.choices[0].message.content
            
            code_match = re.search(r'```python\n(.*?)\n```', generated_code, re.DOTALL)
            if code_match:
                code = code_match.group(1)
            else:
                code = generated_code
            
            typer.echo("Generated Code:")
            typer.echo("=" * 50)
            typer.echo(code)
            typer.echo("=" * 50)
            typer.echo("\nExecution Output:")
            typer.echo("-" * 50)
            
            exec_globals = {}
            exec(code, exec_globals)
            
            typer.echo("-" * 50)
            typer.echo("\n✓ Program executed successfully")
            
        except litellm.APIError as e:
            typer.echo(f"✗ API Error: {str(e)}", err=True)
            raise typer.Exit(code=1)
        except SyntaxError as e:
            typer.echo(f"✗ Syntax Error in generated code: {str(e)}", err=True)
            raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(f"✗ Error: {str(e)}", err=True)
            raise typer.Exit(code=1)
    
    asyncio.run(generate_and_execute())