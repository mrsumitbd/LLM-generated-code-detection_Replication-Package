import requests
from datetime import datetime
from typing import Dict, List, Tuple

def _verify_workflow_runs(
    pr_data: Dict, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, List[str]]:
    """
    Verify that workflow runs occurred for the PR and all 4 jobs ran in parallel.

    Parameters
    ----------
    pr_data : Dict
        Pull request data from the GitHub API. Expected to contain:
        - 'head' : Dict with keys 'ref' (branch name) and 'sha' (commit SHA).
    headers : Dict[str, str]
        HTTP headers for authentication (e.g., {'Authorization': 'token ...'}).
    owner : str
        Repository owner.
    repo : str
        Repository name.

    Returns
    -------
    Tuple[bool, List[str]]
        A tuple where the first element is True if all checks pass, False otherwise.
        The second element is a list of error messages (empty if success).
    """
    errors: List[str] = []

    # Extract branch and commit SHA from PR data
    try:
        head_branch = pr_data["head"]["ref"]
        head_sha = pr_data["head"]["sha"]
    except KeyError as exc:
        errors.append(f"PR data missing expected keys: {exc}")
        return False, errors

    # Fetch workflow runs for the PR branch
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    params = {"head_branch": head_branch, "event": "pull_request"}
    try:
        resp = requests.get(runs_url, headers=headers, params=params)
        resp.raise_for_status()
    except requests.RequestException as exc:
        errors.append(f"Failed to fetch workflow runs: {exc}")
        return False, errors

    runs_data = resp.json()
    workflow_runs = runs_data.get("workflow_runs", [])

    # Filter runs that match the PR commit SHA
    matching_runs = [run for run in workflow_runs if run.get("head_sha") == head_sha]

    if not matching_runs:
        errors.append(f"No workflow runs found for PR #{pr_data.get('number')} on branch '{head_branch}'.")
        return False, errors

    # Helper to parse ISO datetime strings
    def parse_iso(dt_str: str) -> datetime:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")

    # Check each matching run
    for run in matching_runs:
        run_id = run.get("id")
        if run_id is None:
            errors.append("Workflow run missing 'id' field.")
            continue

        jobs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
        try:
            jobs_resp = requests.get(jobs_url, headers=headers)
            jobs_resp.raise_for_status()
        except requests.RequestException as exc:
            errors.append(f"Failed to fetch jobs for run {run_id}: {exc}")
            continue

        jobs_data = jobs_resp.json()
        jobs = jobs_data.get("jobs", [])

        if len(jobs) != 4:
            errors.append(f"Run {run_id} has {len(jobs)} jobs; expected 4.")
            continue

        # Check that all jobs started within 5 seconds of each other
        start_times = []
        for job in jobs:
            started_at = job.get("started_at")
            if not started_at:
                errors.append(f"Job {job.get('id')} in run {run_id} missing 'started_at'.")
                continue
            try:
                start_times.append(parse_iso(started_at))
            except ValueError:
                errors.append(f"Invalid datetime format for job {job.get('id')} in run {run_id}.")
                continue

        if len(start_times) != 4:
            # Already recorded errors for missing/invalid times
            continue

        earliest = min(start_times)
        latest = max(start_times)
        delta_seconds = (latest - earliest).total_seconds()
        if delta_seconds > 5:
            errors.append(
                f"Run {run_id} jobs did not start in parallel: "
                f"time difference {delta_seconds:.1f}s exceeds 5s threshold."
            )

    success = not errors
    return success, errors