def compute_summary(results: GenerateOutputs) -> Dict[str, Any]:
    """Compute aggregated statistics from GenerateOutputs in a format usable by templates.

    This function intentionally does not change layout based on dataset size.
    """
    total_samples = len(results.output_ids)
    total_tokens = sum(len(output_id) for output_id in results.output_ids)
    avg_tokens_per_sample = total_tokens / total_samples
    
    unique_tokens = set()
    for output_id in results.output_ids:
        unique_tokens.update(output_id)
    num_unique_tokens = len(unique_tokens)
    
    return {
        "total_samples": total_samples,
        "total_tokens": total_tokens,
        "avg_tokens_per_sample": avg_tokens_per_sample,
        "num_unique_tokens": num_unique_tokens
    }