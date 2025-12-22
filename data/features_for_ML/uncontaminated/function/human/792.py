import pathlib
from feedback_forensics.data.loader import add_virtual_annotators, get_votes_dict
import gradio as gr
from feedback_forensics.data.dataset_utils import (
    get_annotators_by_type,
    get_available_models,
)
from feedback_forensics.app.constants import (
    NONE_SELECTED_VALUE,
    DEFAULT_ANNOTATOR_VISIBLE_NAME,
    MODEL_IDENTITY_ANNOTATOR_TYPE,
    PRINCIPLE_ANNOTATOR_TYPE,
    PREFIX_PRINICIPLE_FOLLOWING_ANNOTATORS,
    PREFIX_MODEL_IDENTITY_ANNOTATORS,
)

def _get_default_annotator_cols_config(data) -> str:
        """Get the default annotator cols config.

        This sets the annotator columns to the default, and the rows to all principle annotators
        """
        datasets = data[inp["active_datasets_dropdown"]]

        # Normalize datasets to always be a list for processing
        if not isinstance(datasets, list):
            datasets = [datasets] if datasets is not None else []

        # if not dataset is selected, abort
        # (only possible in multidataset selection mode)
        if len(datasets) == 0:
            # need to return something to avoid errors
            # thus returning a dict with no changes/effect
            return {
                inp["annotator_cols_dropdown"]: gr.Dropdown(),
            }

        # Load the full dataset (needed to extract annotator names)
        # which may take a few seconds. Caching ensures this cost is paid only once.
        dataset_config = data[state["avail_datasets"]][datasets[0]]
        results_dir = pathlib.Path(dataset_config.path)
        base_votes_dict = get_votes_dict(results_dir, cache=data[state["cache"]])
        votes_dict = add_virtual_annotators(
            base_votes_dict,
            cache=data[state["cache"]],
            dataset_cache_key=results_dir,
            reference_models=data[inp["reference_models_dropdown"]],
            target_models=[],
        )

        annotator_types = get_annotators_by_type(votes_dict)
        all_annotator_names = []
        model_annotator_names = annotator_types[MODEL_IDENTITY_ANNOTATOR_TYPE][
            "visible_names"
        ]
        model_annotator_names = [
            name.replace(PREFIX_MODEL_IDENTITY_ANNOTATORS, "")
            for name in model_annotator_names
        ]
        for variant, annotators in annotator_types.items():
            all_annotator_names.extend(annotators["visible_names"])

        regular_annotator_names = [
            name
            for name in all_annotator_names
            if PREFIX_MODEL_IDENTITY_ANNOTATORS not in name
            and PREFIX_PRINICIPLE_FOLLOWING_ANNOTATORS not in name
        ]

        return {
            inp["annotator_cols_dropdown"]: gr.Dropdown(
                choices=sorted(all_annotator_names),
                value=[DEFAULT_ANNOTATOR_VISIBLE_NAME],
                interactive=True,
            ),
            inp["annotator_rows_dropdown"]: gr.Dropdown(
                choices=sorted(all_annotator_names),
                value=annotator_types[PRINCIPLE_ANNOTATOR_TYPE]["visible_names"],
                interactive=True,
            ),
            inp["reference_models_dropdown"]: gr.Dropdown(
                choices=sorted(get_available_models(base_votes_dict["df"])),
                value=[],
                interactive=True,
            ),
            inp["models_to_compare_dropdown"]: gr.Dropdown(
                choices=sorted(model_annotator_names),
                value=[],
                interactive=True,
            ),
            inp["annotations_to_compare_dropdown"]: gr.Dropdown(
                choices=sorted(regular_annotator_names),
                value=[DEFAULT_ANNOTATOR_VISIBLE_NAME],
                interactive=True,
            ),
        }