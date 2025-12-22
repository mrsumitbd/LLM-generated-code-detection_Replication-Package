from __future__ import annotations

from typing import Dict

try:
    # Try to import a project‑specific LLM factory if available
    from .llm import get_llm  # type: ignore
except Exception:  # pragma: no cover
    # Fallback to a default OpenAI LLM (requires an API key in the environment)
    try:
        from langchain import OpenAI  # type: ignore
    except Exception:  # pragma: no cover
        # If langchain is not installed, raise a clear error
        raise RuntimeError(
            "Could not import a language model. "
            "Please provide a `get_llm` function or install langchain."
        )
    get_llm = lambda: OpenAI()  # type: ignore

from langchain import PromptTemplate, LLMChain  # type: ignore
from langchain.output_parsers import PydanticOutputParser  # type: ignore


def _call_code_review_llm(
    issue_statement: str,
    project_knowledge: str,
    git_diff: str,
    combined_code_fragments: Dict[str, str],
    *,
    example_output: "CodeReviewModel",
    code_review_parser: PydanticOutputParser,
) -> "CodeReviewModel":
    """
    Call the LLM to produce a code review.

    Parameters
    ----------
    issue_statement : str
        The high‑level description of the issue being addressed.
    project_knowledge : str
        Background information about the project.
    git_diff : str
        The raw git diff for the changes.
    combined_code_fragments : dict[str, str]
        Mapping of file paths to the full code of those files.
    example_output : CodeReviewModel
        An example instance used only for its schema.
    code_review_parser : PydanticOutputParser
        Parser that validates the LLM output against the CodeReviewModel schema.

    Returns
    -------
    CodeReviewModel
        The parsed code review.
    """
    # Format the code fragments into a single string
    fragments_str = "\n".join(
        f"File: {path}\n{code}" for path, code in combined_code_fragments.items()
    )

    # Build the prompt template
    prompt = PromptTemplate(
        input_variables=[
            "issue_statement",
            "project_knowledge",
            "git_diff",
            "combined_code_fragments",
        ],
        template=(
            "You are a senior software engineer reviewing code changes.\n\n"
            "Issue statement:\n{issue_statement}\n\n"
            "Project knowledge:\n{project_knowledge}\n\n"
            "Git diff:\n{git_diff}\n\n"
            "Combined code fragments:\n{combined_code_fragments}\n\n"
            "Please provide a code review in the following JSON format:\n"
            "{format_instructions}"
        ),
    )

    # Get format instructions from the parser
    format_instructions = code_review_parser.get_format_instructions()

    # Create the LLM chain
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain
    raw_output = chain.run(
        issue_statement=issue_statement,
        project_knowledge=project_knowledge,
        git_diff=git_diff,
        combined_code_fragments=fragments_str,
        format_instructions=format_instructions,
    )

    # Parse the output into the CodeReviewModel
    parsed = code_review_parser.parse(raw_output)
    return parsed