def compute_summary(results: GenerateOutputs) -> Dict[str, Any]:
    """Compute aggregated statistics from GenerateOutputs in a format usable by templates.

    This function intentionally does not change layout based on dataset size.
    """
    if not results or not results.outputs:
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "error": 0,
            "pass_rate": 0.0,
            "fail_rate": 0.0,
            "error_rate": 0.0,
            "by_category": {},
            "by_status": {},
        }
    
    total = len(results.outputs)
    passed = 0
    failed = 0
    error = 0
    by_category = {}
    by_status = {"passed": [], "failed": [], "error": []}
    
    for output in results.outputs:
        status = getattr(output, "status", None)
        category = getattr(output, "category", "uncategorized")
        
        if category not in by_category:
            by_category[category] = {"passed": 0, "failed": 0, "error": 0, "total": 0}
        
        by_category[category]["total"] += 1
        
        if status == "passed":
            passed += 1
            by_category[category]["passed"] += 1
            by_status["passed"].append(output)
        elif status == "failed":
            failed += 1
            by_category[category]["failed"] += 1
            by_status["failed"].append(output)
        elif status == "error":
            error += 1
            by_category[category]["error"] += 1
            by_status["error"].append(output)
    
    pass_rate = (passed / total * 100) if total > 0 else 0.0
    fail_rate = (failed / total * 100) if total > 0 else 0.0
    error_rate = (error / total * 100) if total > 0 else 0.0
    
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "error": error,
        "pass_rate": pass_rate,
        "fail_rate": fail_rate,
        "error_rate": error_rate,
        "by_category": by_category,
        "by_status": by_status,
    }