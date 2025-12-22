def _compare_results_report(eval_set: str, left_side: CompareArgs, right_side: CompareArgs, output_format: str):
    if output_format == 'json':
        return json.dumps({
            'eval_set': eval_set,
            'left_side': left_side.to_dict(),
            'right_side': right_side.to_dict()
        })
    elif output_format == 'text':
        return f"Evaluation Set: {eval_set}\nLeft Side: {left_side}\nRight Side: {right_side}"
    else:
        return "Invalid output format specified. Please use 'json' or 'text'."