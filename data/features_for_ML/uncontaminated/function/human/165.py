import json
from deep_next.core.steps.code_review.model.base import CodeReviewModel
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

def _call_code_review_llm(
    issue_statement: str,
    project_knowledge: str,
    git_diff: str,
    combined_code_fragments: dict[str, str],
    *,
    example_output: CodeReviewModel,
    code_review_parser: PydanticOutputParser,
) -> CodeReviewModel:
    messages = [
        ("system", Prompt.role_description),
        ("human", Prompt.issue_statement),
        ("human", Prompt.project_knowledge),
        ("human", Prompt.git_diff),
        ("human", Prompt.code_fragments),
        ("human", Prompt.output_format),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    relevant_code_fragments = "\n\n\n--------------------\n\n\n".join(
        [
            f"# {file_name}:\n\n{combined_code}"
            for file_name, combined_code in combined_code_fragments.items()
        ]
    )

    data = {
        "issue_statement": issue_statement,
        "project_knowledge": project_knowledge,
        "git_diff": git_diff,
        "relevant_code_fragments": relevant_code_fragments,
        "example_output_code_review": json.dumps(example_output.model_dump()),
        "empty_output_code_review": json.dumps({"issues": []}),
    }

    return _invoke_fixable_llm_chain(prompt, data, code_review_parser)