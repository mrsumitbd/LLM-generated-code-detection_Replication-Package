def on_workflow_start(execution_id: str, workflow_id: str, inputs: dict[str, Any]) -> None:
    print(f"Workflow started with execution_id: {execution_id}, workflow_id: {workflow_id}")
    print("Inputs:")
    for key, value in inputs.items():
        print(f"{key}: {value}")