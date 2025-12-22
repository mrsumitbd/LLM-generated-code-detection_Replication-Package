import logging
import ray
from ray.util import list_named_actors

def get_nccl_id_store_by_name(name):
    all_actors = list_named_actors(all_namespaces=True)
    matched_actors = [actor for actor in all_actors if actor.get("name", None) == name]
    if len(matched_actors) == 1:
        actor = matched_actors[0]
        return ray.get_actor(**actor)
    elif len(matched_actors) > 1:
        logging.warning(f"multiple actors with same name found: {matched_actors}")
    elif len(matched_actors) == 0:
        logging.info(f"failed to get any actor named {name}")
    return None