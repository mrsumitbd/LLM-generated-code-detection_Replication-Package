from typing import Any

def compute_source_coverage(
    claims: list[dict[str, Any]], question_references: list[str]
) -> float:
    """Compute the source coverage of the extracted claims."""
    covered_sources = get_relevant_references(claims)
    return (
        covered_sources / len(question_references)
        if len(question_references) > 0
        else 0.0
    )