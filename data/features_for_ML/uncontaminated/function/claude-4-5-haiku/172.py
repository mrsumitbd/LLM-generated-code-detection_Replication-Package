def is_llm_task_result_found(llm_task_results: List[LlmTaskResult], llm_task_name: str) -> bool:
    """
    Check if the llm_task result exists in the llm tasks results file
    """
    return any(task.name == llm_task_name for task in llm_task_results)