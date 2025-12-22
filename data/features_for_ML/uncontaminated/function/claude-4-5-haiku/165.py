def _call_code_review_llm(
    issue_statement: str,
    project_knowledge: str,
    git_diff: str,
    combined_code_fragments: dict[str, str],
    *,
    example_output: CodeReviewModel,
    code_review_parser: PydanticOutputParser,
) -> CodeReviewModel:
    from langchain.llms.base import BaseLLM
    from langchain.prompts import PromptTemplate
    
    llm = BaseLLM()
    
    code_fragments_str = "\n".join(
        f"File: {filename}\n{content}\n"
        for filename, content in combined_code_fragments.items()
    )
    
    prompt_template = PromptTemplate(
        input_variables=[
            "issue_statement",
            "project_knowledge",
            "git_diff",
            "code_fragments",
            "format_instructions",
            "example_output",
        ],
        template="""You are an expert code reviewer. Analyze the following code changes and provide a detailed review.

Issue Statement:
{issue_statement}

Project Knowledge:
{project_knowledge}

Git Diff:
{git_diff}

Code Fragments:
{code_fragments}

{format_instructions}

Example Output Format:
{example_output}

Please provide your code review in the specified JSON format.""",
    )
    
    format_instructions = code_review_parser.get_format_instructions()
    
    prompt = prompt_template.format(
        issue_statement=issue_statement,
        project_knowledge=project_knowledge,
        git_diff=git_diff,
        code_fragments=code_fragments_str,
        format_instructions=format_instructions,
        example_output=example_output.json(),
    )
    
    response = llm.predict(prompt)
    
    code_review = code_review_parser.parse(response)
    
    return code_review