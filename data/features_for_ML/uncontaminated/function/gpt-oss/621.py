from typing import Iterable, Any

def combine(outcomes: Iterable[Any]):
    """
    Combine an iterable of Outcome objects into a single Outcome.

    The function selects the Outcome with the most severe status
    (ERROR > FAIL > PASS > UNTRIED) and merges the `details`
    attributes of all outcomes into the selected one.

    Parameters
    ----------
    outcomes : Iterable[Outcome]
        An iterable of Outcome objects. Each object is expected to
        have a `status` attribute (string) and optionally a
        `details` attribute (iterable).

    Returns
    -------
    Outcome or None
        The combined Outcome, or None if the input iterable is empty.
    """
    # Convert to list to allow multiple passes
    outcomes_list = list(outcomes)
    if not outcomes_list:
        return None

    # Define severity ordering
    severity = {"ERROR": 3, "FAIL": 2, "PASS": 1, "UNTRIED": 0}

    # Find the outcome with the worst status
    worst = outcomes_list[0]
    worst_sev = severity.get(getattr(worst, "status", ""), 0)
    for o in outcomes_list[1:]:
        sev = severity.get(getattr(o, "status", ""), 0)
        if sev > worst_sev:
            worst = o
            worst_sev = sev

    # Merge details if present
    merged_details = []
    for o in outcomes_list:
        details = getattr(o, "details", None)
        if details is not None:
            try:
                merged_details.extend(details)
            except TypeError:
                # If details is not iterable, skip it
                pass

    # If the worst outcome has a `details` attribute, replace it
    if hasattr(worst, "details"):
        try:
            # Try to assign merged details directly
            worst.details = merged_details
        except Exception:
            # If assignment fails, ignore
            pass

    return worst