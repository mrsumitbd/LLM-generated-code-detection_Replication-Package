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
    """List all schedules in the ZenML workspace.

    Args:
        sort_by: The field to sort the schedules by
        page: The page number to return
        size: The number of schedules to return
        created: The creation date of the schedules
        updated: The last update date of the schedules
        name: The name of the schedules
        pipeline_id: The ID of the pipeline
        orchestrator_id: The ID of the orchestrator
        active: Whether the schedule is active
    """
    schedules = get_zenml_client().list_schedules(
        sort_by=sort_by,
        page=page,
        size=size,
        logical_operator=logical_operator,
        created=created,
        updated=updated,
        name=name,
        pipeline_id=pipeline_id,
        orchestrator_id=orchestrator_id,
        active=active,
    )
    return f"""{[schedule.model_dump_json() for schedule in schedules]}"""