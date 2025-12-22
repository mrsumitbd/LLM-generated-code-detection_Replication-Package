def get_task_str(task_type_ind, object_ind, receptacle_ind=None, toggle_ind=None, mrecep_ind=None):
    task_str = ""
    
    if task_type_ind == 0:
        task_str = "PickupObject"
    elif task_type_ind == 1:
        task_str = "PutObject"
    elif task_type_ind == 2:
        task_str = "ToggleObjectOn"
    elif task_type_ind == 3:
        task_str = "ToggleObjectOff"
    elif task_type_ind == 4:
        task_str = "CloseObject"
    elif task_type_ind == 5:
        task_str = "OpenObject"
    elif task_type_ind == 6:
        task_str = "PickupObjectAtLocation"
    elif task_type_ind == 7:
        task_str = "PutObjectAtLocation"
    elif task_type_ind == 8:
        task_str = "PickupObjectRecep"
    elif task_type_ind == 9:
        task_str = "PutObjectInRecep"
    elif task_type_ind == 10:
        task_str = "ToggleObjectInRecepOn"
    elif task_type_ind == 11:
        task_str = "ToggleObjectInRecepOff"
    
    task_str += f"_{object_ind}"
    
    if receptacle_ind is not None:
        task_str += f"_r{receptacle_ind}"
    
    if toggle_ind is not None:
        task_str += f"_t{toggle_ind}"
    
    if mrecep_ind is not None:
        task_str += f"_m{mrecep_ind}"
    
    return task_str