def compute_summary(results: GenerateOutputs) -> Dict[str, Any]:
    summary = {}
    
    summary['total_count'] = len(results)
    summary['min_value'] = min(results)
    summary['max_value'] = max(results)
    summary['average_value'] = sum(results) / len(results)
    
    return summary