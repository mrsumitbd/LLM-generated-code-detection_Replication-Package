from typing import List

def is_llm_task_result_found(llm_task_results: List["LlmTaskResult"], llm_task_name: str) -> bool:
    """
    Check if the llm_task result exists in the llm tasks results file.

    Parameters
    ----------
    llm_task_results : List[LlmTaskResult]
        A list of LlmTaskResult objects.
    llm_task_name : str
        The name of the LLM task to look for.

    Returns
    -------
    bool
        True if a result with the given task name exists, False otherwise.
    """
    for result in llm_task_results:
        # Assume the task name is stored in an attribute called `name`.
        # If the attribute is named differently, adjust accordingly.
        if getattr(result, "name", None) == llm_task_name:
            return True
    return False