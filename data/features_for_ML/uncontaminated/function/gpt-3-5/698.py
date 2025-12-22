def check_finished(goals, pclist):
    return all(goal in pclist for goal in goals)