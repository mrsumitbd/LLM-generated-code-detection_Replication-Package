def check_finished(goals, pclist):
    max_sr = 0
    for goal in goals:
        sr = 0
        for subgoal in goal:
            if 'another_obj2_uid' in subgoal:
                pcd3 = pclist[subgoal['another_obj2_uid']]
            else:
                pcd3 = None
            if check_subgoal_finished_rigid(
                subgoal, pclist[subgoal['obj1_uid']], pclist[subgoal['obj2_uid']], pcd3
            ):
                sr += 1 / len(goal)
        max_sr = max(max_sr, sr)
    return max_sr