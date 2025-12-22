import os
import json
import numpy as np
from typing import Annotated
import typer
import click
from .constants import TASK_NAMES_TO_YAML, SAMPLING_PARAMS_DEFAULT
from .backends import Backend
from .utils import get_system_prompt_keys

def evaluate(
    ctx: typer.Context,
    task: Annotated[
        str,
        typer.Option(
            ...,
            help="Task to process.",
            click_type=click.Choice(list(TASK_NAMES_TO_YAML.keys())),
            case_sensitive=False,
        ),
    ],
    model: Annotated[str, typer.Option(..., help="The model to run")],
    backend: Annotated[
        Backend,
        typer.Option(
            help="Backend to use for inference.",
            case_sensitive=False,
        ),
    ] = Backend.VLLM,
    backend_args: Annotated[
        str,
        typer.Option(
            help="Backend parameters to use for inference.",
            case_sensitive=False,
        ),
    ] = "",
    sampling_params: Annotated[
        str,
        typer.Option(
            help="Sampling parameters to use for inference.",
            case_sensitive=False,
        ),
    ] = SAMPLING_PARAMS_DEFAULT,
    result_dir: Annotated[
        str,
        typer.Option(
            help="Result directory to save outputs.",
        ),
    ] = "./",
    system_prompt_name: Annotated[
        str,
        typer.Option(
            help="System prompt template to use, overriding any pre-configured system prompt for this model.",
            click_type=click.Choice(get_system_prompt_keys()),
        ),
    ] = None,
    system_prompt: Annotated[
        str,
        typer.Option(
            help="System prompt to use, overriding any pre-configured system prompt for this model."
        ),
    ] = None,
    n: Annotated[
        int, typer.Option(help="Number of samples generated per problem.")
    ] = None,
    seed: Annotated[int, typer.Option(help="Random seed.")] = 41,
    assistant_prefill: Annotated[
        str,
        typer.Option(
            help=r'Assistant prefill for the model response, overriding any pre-configured assistant prefill for this model. Ex: "<think>\n"'
        ),
    ] = None,
    as_test: Annotated[
        bool, typer.Option(help="Perform a test run on 10 samples of the dataset.")
    ] = False,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing results.")
    ] = False,
    batch_size: Annotated[
        int,
        typer.Option(
            help="Batch size for inference. only applicable for the vllm backend."
        ),
    ] = 64,
):
    # Implement the function logic here
    pass