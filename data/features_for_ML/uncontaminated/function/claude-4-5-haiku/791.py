def _verify_workflow_runs(
    pr_data: Dict, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, List[str]]:
    """Verify that workflow runs occurred for the PR and all 4 jobs ran in parallel."""
    import requests
    from datetime import datetime, timedelta
    
    errors = []
    
    try:
        # Get the PR head commit SHA
        head_sha = pr_data.get("head", {}).get("sha")
        if not head_sha:
            errors.append("Could not find head SHA in PR data")
            return False, errors
        
        # Get workflow runs for this commit
        runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
        params = {"head_sha": head_sha}
        
        runs_response = requests.get(runs_url, headers=headers, params=params)
        runs_response.raise_for_status()
        runs_data = runs_response.json()
        
        workflow_runs = runs_data.get("workflow_runs", [])
        
        if not workflow_runs:
            errors.append(f"No workflow runs found for commit {head_sha}")
            return False, errors
        
        # Check each workflow run
        all_jobs_ran = True
        for run in workflow_runs:
            run_id = run.get("id")
            
            # Get jobs for this run
            jobs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
            jobs_response = requests.get(jobs_url, headers=headers)
            jobs_response.raise_for_status()
            jobs_data = jobs_response.json()
            
            jobs = jobs_data.get("jobs", [])
            
            if len(jobs) < 4:
                errors.append(f"Run {run_id} has {len(jobs)} jobs, expected 4")
                all_jobs_ran = False
                continue
            
            # Check if jobs ran in parallel by comparing start times
            start_times = []
            for job in jobs:
                started_at = job.get("started_at")
                if started_at:
                    start_times.append(datetime.fromisoformat(started_at.replace("Z", "+00:00")))
            
            if len(start_times) >= 2:
                # Check if jobs started within a reasonable time window (e.g., 1 minute)
                time_diff = max(start_times) - min(start_times)
                if time_diff > timedelta(minutes=1):
                    errors.append(f"Run {run_id}: Jobs did not start in parallel (time diff: {time_diff})")
                    all_jobs_ran = False
        
        if not all_jobs_ran:
            return False, errors
        
        return True, []
        
    except requests.RequestException as e:
        errors.append(f"API request failed: {str(e)}")
        return False, errors
    except Exception as e:
        errors.append(f"Error verifying workflow runs: {str(e)}")
        return False, errors