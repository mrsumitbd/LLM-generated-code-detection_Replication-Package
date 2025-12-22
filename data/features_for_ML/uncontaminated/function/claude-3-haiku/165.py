def _call_code_review_llm(
    issue_statement: str,
    project_knowledge: str,
    git_diff: str,
    combined_code_fragments: dict[str, str],
    *,
    example_output: CodeReviewModel,
    code_review_parser: PydanticOutputParser,
) -> CodeReviewModel:
    prompt = f"Issue statement: {issue_statement}\n\nProject knowledge: {project_knowledge}\n\nGit diff:\n{git_diff}\n\nCode fragments:\n{combined_code_fragments}"
    model_output = example_output.copy()
    model_output = code_review_parser.parse(prompt, model_output)
    return model_output