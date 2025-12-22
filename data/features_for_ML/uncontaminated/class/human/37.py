
class WorkflowRun:
    """Immutable data transfer object for workflow context.

    This DTO safely passes workflow context data between components without
    creating tight coupling or state conflicts.
    """

    workflow_definition_name: str
    workflow_run_id: str