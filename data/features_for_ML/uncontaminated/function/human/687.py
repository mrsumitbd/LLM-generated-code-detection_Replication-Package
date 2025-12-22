import pandas as pd
import gradio as gr
import feedback_forensics.app.plotting
from feedback_forensics.app.constants import (
    NONE_SELECTED_VALUE,
    APP_BASE_URL,
    PREFIX_MODEL_IDENTITY_ANNOTATORS,
    PREFIX_PRINICIPLE_FOLLOWING_ANNOTATORS,
)
from feedback_forensics.app.url_parser import (
    get_config_from_query_params,
    get_url_with_query_params,
    get_list_member_from_url_string,
    transfer_url_str_to_nonurl_str,
    transfer_url_list_to_nonurl_list,
    parse_list_param,
)
from feedback_forensics.data.handler import (
    DatasetHandler,
    _get_annotator_df_col_names,
)

def load_data(
        data: dict,
    ) -> dict:
        """Load data with dictionary inputs instead of individual arguments."""
        datasets = data[inp["active_datasets_dropdown"]]

        # Normalize datasets to always be a list for processing
        if not isinstance(datasets, list):
            datasets = [datasets] if datasets is not None else []

        cache = data[state["cache"]]
        split_col = data[inp["split_col_dropdown"]]
        selected_vals = data[inp["split_col_selected_vals_dropdown"]]
        reference_models = data[inp["reference_models_dropdown"]]
        metric_name = data[inp["metric_name_dropdown"]]
        sort_by = data[inp["sort_by_dropdown"]]
        sort_ascending = data[inp["sort_order_dropdown"]] == "Ascending"

        if len(datasets) == 0:
            gr.Warning(
                "No datasets selected. Please select at least one dataset to run analysis on.",
            )
            return {
                out["overall_metrics_table"]: gr.Dataframe(
                    value=pd.DataFrame(), headers=["No data available"]
                ),
                out["annotator_table"]: gr.Dataframe(
                    value=pd.DataFrame(), headers=["No data available"]
                ),
                out["share_link"]: data.get(
                    state["app_url"], ""
                ),  # Return base URL or empty string
            }

        # loading data via handler
        gr.Info(f"Loading data for: {', '.join(datasets)}...", duration=3)
        dataset_handler = DatasetHandler(
            cache=cache,
            avail_datasets=data[state["avail_datasets"]],
            reference_models=reference_models,
        )
        dataset_handler.load_data_from_names(datasets)

        # set annotators rows and columns according to user input
        annotator_rows_visible_names = data[inp["annotator_rows_dropdown"]]
        dataset_handler.set_annotator_rows(annotator_rows_visible_names)
        annotator_cols_visible_names = data[inp["annotator_cols_dropdown"]]
        if len(datasets) > 1 and len(annotator_cols_visible_names) > 1:
            gr.Warning(
                (
                    "Only one annotator column (e.g. for model identity) is supported"
                    " when selecting multiple datasets. Only using first annotator column"
                    f" ({annotator_cols_visible_names[0]})."
                ),
            )
            avail_annotators_cross_datasets = (
                dataset_handler.get_available_annotator_visible_names()
            )
            annotator_cols_visible_names = annotator_cols_visible_names[:1]
            if annotator_cols_visible_names[0] not in avail_annotators_cross_datasets:
                gr.Warning(
                    (
                        f"Annotator column '{annotator_cols_visible_names[0]}' not"
                        " found in across all selected datasets. Please select a "
                        "different annotator column. Aborting analysis."
                    )
                )
                # return statement needs to have at least one output
                # thus we add this output without change
                return {
                    inp["split_col_dropdown"]: data[inp["split_col_dropdown"]],
                    out["overall_metrics_table"]: gr.Dataframe(
                        value=pd.DataFrame(), headers=["⛔️ Analysis stopped"]
                    ),
                    out["annotator_table"]: gr.Dataframe(
                        value=pd.DataFrame(), headers=["⛔️ Analysis stopped"]
                    ),
                }

        dataset_handler.set_annotator_cols(annotator_cols_visible_names)

        # checking if splitting by column is requested
        if split_col != NONE_SELECTED_VALUE and split_col is not None:
            if dataset_handler.num_cols > 1:
                raise gr.Error(
                    "Only one votes_df is supported when splitting by column"
                )

            # set values equivalent to no value to None
            if selected_vals == [] or set(selected_vals) == set(
                inp["split_col_selected_vals_dropdown"].choices
            ):
                selected_vals = None

            # split the first dataset (handler) by the selected column
            # this now is treated like multiple datasets (as in multiple columns)
            dataset_handler.split_by_col(col=split_col, selected_vals=selected_vals)

        # compute metrics
        overall_metrics = dataset_handler.get_overall_metrics()
        annotator_metrics = dataset_handler.get_annotator_metrics()

        # set up sorting of annotator metrics table
        sort_by_choices = ["Max diff"] + list(annotator_metrics.keys())
        if sort_by not in sort_by_choices and sort_by_choices:
            # might be url encoded version of sort_by
            sort_by = transfer_url_str_to_nonurl_str(sort_by, sort_by_choices)
            if sort_by is None:
                sort_by = sort_by_choices[0]

        # generate Gradio (not pandas) dataframes (shown as tables in the app)
        tables = feedback_forensics.app.plotting.generate_dataframes(
            annotator_metrics=annotator_metrics,
            overall_metrics=overall_metrics,
            metric_name=metric_name,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
        )

        data[state["votes_dicts"]] = dataset_handler.votes_dicts

        return_dict = {
            out["overall_metrics_table"]: tables["overall_metrics"],
            out["annotator_table"]: tables["annotator"],
            state["cache"]: cache,
            state["computed_overall_metrics"]: overall_metrics,
            state["computed_annotator_metrics"]: annotator_metrics,
            state[
                "default_annotator_cols"
            ]: dataset_handler.first_handler.default_annotator_cols,
            state[
                "default_annotator_rows"
            ]: dataset_handler.first_handler.default_annotator_rows,
            state["votes_dicts"]: dataset_handler.votes_dicts,
            inp["metric_name_dropdown"]: gr.Dropdown(
                value=metric_name,
                interactive=True,
            ),
            inp["sort_by_dropdown"]: gr.Dropdown(
                choices=sort_by_choices, value=sort_by
            ),
            inp["sort_order_dropdown"]: gr.Dropdown(
                value="Descending" if not sort_ascending else "Ascending"
            ),
            **example_viewer_callbacks["update_example_viewer_options"](data),
        }

        # generate share link based on updated app state data
        for key in [
            state["computed_annotator_metrics"],
            state["computed_overall_metrics"],
            state["default_annotator_cols"],
            state["default_annotator_rows"],
            state["votes_dicts"],
        ]:
            data[key] = return_dict[key]

        return_dict[out["share_link"]] = _get_url_share_link_from_app_state(data)

        return return_dict