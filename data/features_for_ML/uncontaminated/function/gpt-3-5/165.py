def _call_code_review_llm(
    issue_statement: str,
    project_knowledge: str,
    git_diff: str,
    combined_code_fragments: dict[str, str],
    *,
    example_output: CodeReviewModel,
    code_review_parser: PydanticOutputParser,
) -> CodeReviewModel:
    
    # Implementation code here
    
    return example_output