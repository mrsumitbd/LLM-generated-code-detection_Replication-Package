def _verify_workflow_runs(pr_data: Dict, headers: Dict[str, str], owner: str, repo: str) -> Tuple[bool, List[str]]:
    pr_number = pr_data.get('number')
    workflow_runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?event=pull_request&pull_request={pr_number}"
    
    response = requests.get(workflow_runs_url, headers=headers)
    if response.status_code != 200:
        return False, []
    
    workflow_runs = response.json().get('workflow_runs', [])
    
    job_names = set()
    for run in workflow_runs:
        if run.get('status') == 'completed' and run.get('conclusion') == 'success':
            jobs = run.get('jobs', [])
            for job in jobs:
                job_names.add(job.get('name'))
    
    return len(job_names) == 4, list(job_names)