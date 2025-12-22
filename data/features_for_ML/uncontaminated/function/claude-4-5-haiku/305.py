def compute_source_coverage(
    claims: list[dict[str, Any]], question_references: list[str]
) -> float:
    """Compute the source coverage of the extracted claims."""
    if not question_references:
        return 0.0
    
    if not claims:
        return 0.0
    
    covered_sources = set()
    
    for claim in claims:
        if isinstance(claim, dict) and "source" in claim:
            source = claim["source"]
            if source in question_references:
                covered_sources.add(source)
    
    coverage = len(covered_sources) / len(question_references)
    return coverage