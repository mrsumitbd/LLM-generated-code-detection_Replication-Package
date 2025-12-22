def is_llm_task_result_found(llm_task_results: List[LlmTaskResult], llm_task_name: str) -> bool:
    for result in llm_task_results:
        if result.llm_task_name == llm_task_name:
            return True
    return False