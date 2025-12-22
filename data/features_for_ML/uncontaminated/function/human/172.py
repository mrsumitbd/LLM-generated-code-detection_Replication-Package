from typing import List
from simpleval.testcases.schemas.llm_task_result import LlmTaskResult

def is_llm_task_result_found(llm_task_results: List[LlmTaskResult], llm_task_name: str) -> bool:
    """
    Check if the llm_task result exists in the llm tasks results file
    """
    results = {result.name: result for result in llm_task_results}
    return llm_task_name in results