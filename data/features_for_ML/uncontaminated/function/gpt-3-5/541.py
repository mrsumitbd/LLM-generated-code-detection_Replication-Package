from typing import List, Any, Union, Dict, Optional
from pathlib import Path
import json

def export_traces_json(traces: List[Any], output_path: Union[str, Path], metadata: Optional[Dict[str, Any]] = None) -> None:
    data = [trace.to_dict() for trace in traces]
    if metadata:
        data.append(metadata)
    
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)