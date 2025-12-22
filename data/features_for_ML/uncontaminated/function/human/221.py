import os
import click
import typer
from typing_extensions import Annotated
from skythought.evals.common.entities import (
    Backend,
    BackendParameters,
    SamplingParameters,
)
from skythought.evals.inference_and_check import (
    generate_and_save,
    generate_and_score,
    score_results,
)
from skythought.evals.models import ModelConfig, get_system_prompt_keys
from skythought.evals.tasks import TASK_HANDLER_MAP, TASK_NAMES_TO_YAML, TaskConfig
from skythought.evals.util.common import set_seed

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
    set_seed(seed)

    (
        task,
        _,
        model,
        backend,
        backend_args_as_dict,
        backend_params,
        sampling_params_as_dict,
        sampling_params,
        n,
        batch_size,
        system_prompt,
        assistant_prefill,
    ) = parse_common_args(
        task=task,
        model=model,
        # `evaluate` does not allow customization of `task_args`
        task_args="",
        backend=backend,
        backend_args=backend_args,
        sampling_params=sampling_params,
        n=n,
        batch_size=batch_size,
        system_prompt=system_prompt,
        assistant_prefill=assistant_prefill,
    )
    # ensure parsing was correct
    assert isinstance(sampling_params, SamplingParameters)
    logger.info(
        f"Temperature: {sampling_params.params.temperature}, top_p: {sampling_params.params.top_p}, max_tokens: {sampling_params.params.max_tokens}"
    )

    start = 0
    end = -1
    if as_test:
        start = 0
        end = 10
        sampling_params.params.max_tokens = 2048
        logger.info("Running test run with 10 samples and max tokens set to 2048.")

    task_config = TaskConfig.from_yaml(TASK_NAMES_TO_YAML[task])
    handler_name = task_config.handler
    handler_cls = TASK_HANDLER_MAP[handler_name]
    handler = handler_cls(task_config)

    model_config = ModelConfig.from_model_id(
        model, system_prompt_name, system_prompt, assistant_prefill
    )

    run_config_dict = get_run_config(
        task,
        task_config,
        model_config,
        backend,
        backend_args_as_dict,
        sampling_params_as_dict,
        start,
        end,
    )

    output_dir = get_output_dir(
        result_dir,
        model_id=model,
        task=task,
        start=start,
        end=end,
        run_config=run_config_dict,
    )
    if not overwrite and output_dir.exists() and len(os.listdir(output_dir)) != 0:
        raise ValueError(
            f"Output directory {output_dir} already exists. pass `--overwrite` to overwrite."
        )
    # create result dir if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_and_score(
        handler,
        model_config,
        backend,
        backend_params,
        sampling_params,
        output_dir,
        start,
        end,
        run_config_dict,
        batch_size=batch_size,
    )