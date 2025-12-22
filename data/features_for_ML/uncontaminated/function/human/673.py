from alfworld.gen import constants
import random
from alfworld.gen import goal_library as glib

def get_task_str(task_type_ind, object_ind, receptacle_ind=None, toggle_ind=None, mrecep_ind=None):
    goal_str = constants.pddl_goal_type
    if constants.data_dict['pddl_params']['object_sliced']:
        goal_str += "_slice"
    template = random.choice(glib.gdict[goal_str]['templates'])
    obj = constants.OBJECTS[object_ind].lower()
    recep = constants.OBJECTS[receptacle_ind].lower() if receptacle_ind is not None else ""
    tog = constants.OBJECTS[toggle_ind].lower() if toggle_ind is not None else ""
    mrecep = constants.OBJECTS[mrecep_ind].lower() if mrecep_ind is not None else ""
    filled_in_str = template.format(obj=obj, recep=recep, toggle=tog, mrecep=mrecep)
    return filled_in_str