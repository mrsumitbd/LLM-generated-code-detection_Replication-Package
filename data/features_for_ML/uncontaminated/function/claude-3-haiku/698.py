def check_finished(goals, pclist):
    for goal in goals:
        if goal not in pclist:
            return False
    return True