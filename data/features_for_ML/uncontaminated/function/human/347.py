import pandas as pd
import numpy as np

def load_study(study_name: str) -> pd.DataFrame:
    # load the study
    df: pd.DataFrame = download_study(study_name)
    set_from_flow(df)

    # ensure columns "values_0" and "values_1" are float dtypes
    df["values_0"] = df["values_0"].astype(float)
    df["values_1"] = df["values_1"].astype(float)

    is_cost = is_cost_objective(df)
    if is_cost:
        df["values_1"] = 100 * 100 * df["values_1"]

    # clean-up unused parameters to be N/A
    if "params_retriever" in df.columns:
        df.loc[df["params_retriever"] == "sparse", "params_embedding_model"] = np.nan

    # clean-up missing trials by re-numbering them
    df.sort_values(by="datetime_complete", inplace=True)
    df["number"] = range(1, len(df) + 1)

    # remember which study this is
    df["study_name"] = study_name

    # pre-calculate some useful columns
    df["compute_hours"] = (df["duration"].dt.total_seconds() / 3600).cumsum()
    df["wallclock_hours"] = (
        df["datetime_complete"] - df["datetime_start"].min()
    ) / pd.Timedelta(hours=1)

    # ensure exception columns exist
    for col in [
        "user_attrs_metric_exception_class",
        "user_attrs_metric_exception",
        "user_attrs_metric_exception_message",
    ]:
        if col not in df.columns:
            df[col] = "None"

    # ensure run status columns exist
    for col in [
        "user_attrs_is_seeding",
        "user_attrs_metric_is_pruned",
        "user_attrs_metric_failed",
    ]:
        if col not in df.columns:
            df[col] = pd.NA

    # ensure error counts exist
    for col in ["user_attrs_metric_num_errors", "user_attrs_metric_num_total"]:
        if col not in df.columns:
            df[col] = 0

    # clean-up synthesizer parameters
    if (
        "params_no_rag_response_synthesizer_llm" in df.columns
        and "params_no_rag_llm_name" in df.columns
    ):
        df["params_response_synthesizer_llm"] = df[
            "params_no_rag_response_synthesizer_llm"
        ].fillna(df["params_no_rag_llm_name"])
        df = df.drop(columns=["params_no_rag_llm_name"])
    elif "params_no_rag_llm_name" in df.columns:
        df = df.rename(
            columns={"params_no_rag_llm_name": "params_response_synthesizer_llm"}
        )

    # remove invalid data (but why are they missing?)
    # Frequent restarting left the DB with some cases of missing data that had to be excluded.
    bad_rag_mode_mas = df["params_rag_mode"].isna()
    n_bad_rag_mode = bad_rag_mode_mas.sum()
    if n_bad_rag_mode > 0:
        print(f"WARNING: {n_bad_rag_mode} trials with missing RAG mode were excluded.")
        df = df[~bad_rag_mode_mas]

    return df