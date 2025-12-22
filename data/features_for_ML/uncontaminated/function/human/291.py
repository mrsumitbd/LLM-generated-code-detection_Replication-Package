from typing import Literal, Optional, Dict, Any, Union

def _prepare_parameters(
    *,
    outputs: Any,
    reference_outputs: Any,
    rubric: Dict[str, str],
    exclude_keys: list[str],
    use_reasoning: bool,
    list_match_mode: Literal[
        "superset", "subset", "same_elements", "ordered"
    ] = "same_elements",
):
    json_schema: dict = {
        "type": "object",
        "title": "structured_match_score",
        "description": "Scores measuring the accuracy of structured outputs",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }

    scores = {}
    formatted_rubric = ""
    use_list_reducer = False

    if isinstance(outputs, list):
        use_list_reducer = True
        if not isinstance(reference_outputs, list):
            raise ValueError(
                "If outputs is a list, reference_outputs must also be a list"
            )

        # Create mapping dictionaries
        outputs_to_use = {}
        reference_outputs_to_use = {}

        if list_match_mode == "ordered":
            # Outputs/Reference outputs must be in the same order
            for i in range(len(outputs)):
                for key, value in outputs[i].items():
                    outputs_to_use[f"{key}_{i}"] = value
            for i in range(len(reference_outputs)):
                for key, value in reference_outputs[i].items():
                    reference_outputs_to_use[f"{key}_{i}"] = value

        elif list_match_mode == "superset":
            # Match each reference output to the best matching output
            available_outputs = list(range(len(outputs)))
            matched_references = set()

            for i, ref_item in enumerate(reference_outputs):
                best_match_score = -1

                # Try each available output item
                for out_idx in available_outputs:
                    output_item = outputs[out_idx]

                    # Calculate match score based on exact matches of keys
                    match_score = 0
                    for key in ref_item:
                        if (
                            key in output_item
                            and key not in exclude_keys
                            and key not in rubric
                        ):
                            match_score += int(ref_item[key] == output_item[key])

                    # If this is the best match so far, update
                    if match_score > best_match_score:
                        best_match_score = match_score
                        best_match_idx = out_idx

                # If we found a match, use it
                if best_match_idx is not None:
                    for key, value in outputs[best_match_idx].items():
                        outputs_to_use[f"{key}_{i}"] = value

                    for key, value in ref_item.items():
                        reference_outputs_to_use[f"{key}_{i}"] = value

                    # Remove the used output from available options
                    available_outputs.remove(best_match_idx)
                    matched_references.add(i)
                else:
                    # There were extra reference items
                    for key, value in ref_item.items():
                        reference_outputs_to_use[f"{key}_{i}"] = value

        else:  # "same_items" or "subset"
            # Match each output to the best matching reference
            available_references = list(range(len(reference_outputs)))
            matched_outputs = set()

            for i, output_item in enumerate(outputs):
                best_match_idx = None
                best_match_score = -1

                # Try each available reference item
                for ref_idx in available_references:
                    ref_item = reference_outputs[ref_idx]

                    # Calculate match score based on exact matches of keys
                    match_score = 0
                    for key in output_item:
                        if (
                            key in ref_item
                            and key not in exclude_keys
                            and key not in rubric
                        ):
                            match_score += int(output_item[key] == ref_item[key])

                    # If this is the best match so far, update
                    if match_score > best_match_score:
                        best_match_score = match_score
                        best_match_idx = ref_idx

                # If we found a match, use it
                if best_match_idx is not None:
                    for key, value in output_item.items():
                        outputs_to_use[f"{key}_{i}"] = value

                    for key, value in reference_outputs[best_match_idx].items():
                        reference_outputs_to_use[f"{key}_{i}"] = value

                    # Remove the used reference from available options
                    available_references.remove(best_match_idx)
                    matched_outputs.add(i)
                else:
                    # There were extra output items
                    for key, value in output_item.items():
                        outputs_to_use[f"{key}_{i}"] = value

            # For "same_elements" mode: penalize unmatched references
            if list_match_mode == "same_elements":
                for ref_idx in available_references:
                    ref_item = reference_outputs[ref_idx]
                    dummy_idx = len(outputs) + available_references.index(ref_idx)
                    for key, value in ref_item.items():
                        reference_outputs_to_use[f"{key}_{dummy_idx}"] = value

        outputs = outputs_to_use
        reference_outputs = reference_outputs_to_use

    for raw_key, value in outputs.items():
        if use_list_reducer:
            key = raw_key[: raw_key.rfind("_")]
        else:
            key = raw_key
        if key in exclude_keys:
            continue
        if raw_key not in reference_outputs:
            scores[raw_key] = 0
            continue
        if key not in rubric and reference_outputs[raw_key] == value:
            scores[raw_key] = 1
        elif key not in rubric:
            scores[raw_key] = 0
        else:
            key_criteria = rubric[key]
            formatted_rubric += f"Key: {key}, Criteria: {key_criteria}\n"
            if not use_reasoning:
                json_schema["properties"][raw_key] = {
                    "type": "boolean",
                    "description": f"Does the output for key {key}, follow the criteria? {key_criteria}",
                }
            else:
                json_schema["properties"][raw_key] = {
                    "type": "object",
                    "properties": {
                        "reasoning": {
                            "type": "string",
                            "description": f"Reasoning for the score you assigned to key {key}",
                        },
                        "score": {
                            "type": "boolean",
                            "description": f"Does the output for key {key}, follow the criteria? {key_criteria}",
                        },
                    },
                    "required": ["score", "reasoning"],
                    "additionalProperties": False,
                }

    for raw_key, value in reference_outputs.items():
        if use_list_reducer:
            key = raw_key[: raw_key.rfind("_")]
        else:
            key = raw_key
        if key not in exclude_keys and raw_key not in outputs:
            scores[raw_key] = 0

    return (
        outputs,
        reference_outputs,
        json_schema,
        scores,
        formatted_rubric,
        use_list_reducer,
    )