import json
from derisk._private.pydantic import BaseModel
from typing import Any, Dict, Union, Optional, List, Type

def _bm_to_str(bms: Optional[List]):
            if bms:
                if isinstance(bms[0], BaseModel):
                    return json.dumps([item.to_dict() for item in bms], ensure_ascii=False)
                elif hasattr(bms[0], "__dict__"):
                    return json.dumps([item.__dict__ for item in bms], ensure_ascii=False)
                else:
                    return json.dumps([item for item in bms], ensure_ascii=False)
            else:
                return None