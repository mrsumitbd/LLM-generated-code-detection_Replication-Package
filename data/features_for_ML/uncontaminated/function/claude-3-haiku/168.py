import asyncio
import os
import tempfile
import typer
from langchain.agents import create_openai_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import PythonREPLTool
from langchain.utilities import PythonREPLWrapper

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
    async def generate_and_execute():
        llm = OpenAI(model_name=model, max_tokens=max_tokens)
        prompt = PromptTemplate(
            input_variables=["task"],
            template="Write a Python program to {task}.",
        )
        agent = create_openai_agent(llm, PythonREPLTool())
        result = await agent.arun(prompt.format(task=task))

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(result)
            temp_file.flush()
            os.system(f"python {temp_file.name}")

    asyncio.run(generate_and_execute())