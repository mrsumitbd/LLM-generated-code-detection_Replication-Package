def compute_source_coverage(claims: list[dict[str, Any]], question_references: list[str]) -> float:
    total_claims = len(claims)
    covered_claims = sum(1 for claim in claims if any(ref in claim['source'] for ref in question_references))
    
    if total_claims == 0:
        return 0.0
    else:
        return covered_claims / total_claims * 100.0