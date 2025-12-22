from derisk.util.json_utils import serialize
import json

def _format_vis_msg(msg: str):
    content = json.dumps({"vis": msg}, default=serialize, ensure_ascii=False)
    return f"data:{content} \n"