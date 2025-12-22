from yacs.config import CfgNode as CN

def create_cfg_recursive(cfg, task_args_dict: dict):
        for task, subtasks in task_args_dict.items():
            if isinstance(subtasks, dict):
                setattr(cfg, task, CN())
                task_cfg = getattr(cfg, task)
                create_cfg_recursive(task_cfg, dict(subtasks.items()))
            else:
                setattr(cfg, task, None)