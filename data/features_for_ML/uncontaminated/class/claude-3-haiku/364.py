from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class ExecutionState:
    """Represents the current execution state of a workflow"""
    workflow_id: str
    task_states: Dict[str, 'TaskState'] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    status: str = 'RUNNING'

    def __post_init__(self):
        pass