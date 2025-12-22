def check_finished(goals, pclist):
    """
    Return True if every element in `goals` is present in `pclist`,
    otherwise return False.  The comparison is performed using the
    standard equality operator.  If either argument is None, it is
    treated as an empty sequence.
    """
    if goals is None:
        goals = []
    if pclist is None:
        pclist = []

    # Convert pclist to a set for efficient membership tests
    pcl_set = set(pclist)

    for g in goals:
        if g not in pcl_set:
            return False
    return True