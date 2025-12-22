import requests

def _verify_workflow_runs(
    pr_data: Dict, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, List[str]]:
    """Verify that workflow runs occurred for the PR and all 4 jobs ran in parallel."""
    pull_number = pr_data["number"]
    workflow_runs = []
    all_jobs_ran = True
    error_messages = []

    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/actions/runs?event=pull_request&pull_request={pull_number}",
            headers=headers,
        )
        response.raise_for_status()
        workflow_runs = response.json()["workflow_runs"]

        if len(workflow_runs) < 1:
            all_jobs_ran = False
            error_messages.append("No workflow runs found for the PR.")
        else:
            job_counts = [run["jobs_count"] for run in workflow_runs]
            if any(count != 4 for count in job_counts):
                all_jobs_ran = False
                error_messages.append("Not all 4 jobs ran in parallel for the PR.")
    except requests.exceptions.RequestException as e:
        all_jobs_ran = False
        error_messages.append(str(e))

    return all_jobs_ran, error_messages