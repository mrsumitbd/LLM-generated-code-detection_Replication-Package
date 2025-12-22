def list_schedules(
    sort_by: str = "desc:created",
    page: int = 1,
    size: int = 10,
    logical_operator: str = "and",
    created: str = None,
    updated: str = None,
    name: str = None,
    pipeline_id: str = None,
    orchestrator_id: str = None,
    active: bool = None,
) -> str:
    return f"Listing schedules with sort_by={sort_by}, page={page}, size={size}, logical_operator={logical_operator}, created={created}, updated={updated}, name={name}, pipeline_id={pipeline_id}, orchestrator_id={orchestrator_id}, active={active}"