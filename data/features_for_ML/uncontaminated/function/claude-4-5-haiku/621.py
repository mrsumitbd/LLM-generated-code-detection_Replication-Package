def combine(outcomes: Iterable[Outcome]):
    outcomes_list = list(outcomes)
    
    if not outcomes_list:
        yield {}
        return
    
    first, *rest = outcomes_list
    
    for outcome in first:
        for rest_outcome in combine(rest):
            combined = {**outcome, **rest_outcome}
            yield combined