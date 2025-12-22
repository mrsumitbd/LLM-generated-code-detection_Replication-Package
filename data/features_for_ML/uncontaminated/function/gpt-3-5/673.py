def get_task_str(task_type_ind, object_ind, receptacle_ind=None, toggle_ind=None, mrecep_ind=None):
    task_str = f"{task_type_ind}-{object_ind}"
    if receptacle_ind is not None:
        task_str += f"-{receptacle_ind}"
    if toggle_ind is not None:
        task_str += f"-{toggle_ind}"
    if mrecep_ind is not None:
        task_str += f"-{mrecep_ind}"
    return task_str