from typing import (
    Any,
    Callable,
    Literal,
    NamedTuple,
    Optional,
    get_args,
)

def get_differentiable_paths(
    apply_endpoint_fn: Callable, inputs: dict[str, Any], outputs: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Get the paths of all differentiable leaves present in the given inputs and outputs."""
    InputSchema = get_input_schema(apply_endpoint_fn)
    OutputSchema = get_output_schema(apply_endpoint_fn)

    diffable_input_paths = InputSchema.differentiable_arrays
    diffable_output_paths = OutputSchema.differentiable_arrays

    ad_inputs = []
    for pattern in diffable_input_paths:
        ad_inputs.extend(expand_path_pattern(pattern, inputs))

    ad_outputs = []
    for pattern in diffable_output_paths:
        ad_outputs.extend(expand_path_pattern(pattern, outputs))

    return ad_inputs, ad_outputs