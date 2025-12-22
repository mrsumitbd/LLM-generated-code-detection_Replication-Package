def compute_source_coverage(
    claims: list[dict[str, Any]], question_references: list[str]
) -> float:
    """Compute the source coverage of the extracted claims."""
    if not claims or not question_references:
        return 0.0

    unique_sources = set()
    for claim in claims:
        unique_sources.add(claim["source"])

    return len(unique_sources) / len(question_references)