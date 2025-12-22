from typing import Dict, List, Optional, Tuple
import datetime

def _verify_workflow_runs(
    pr_data: Dict, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, List[str]]:
    """Verify that workflow runs occurred for the PR and all 4 jobs ran in parallel."""
    print("\n⚙️ Verifying workflow runs...")
    errors = []

    pr_number = pr_data["number"]

    # Get workflow runs for the PR
    success, runs_response = _get_github_api(
        "actions/runs?event=pull_request&per_page=50", headers, owner, repo
    )

    if not success:
        return False, ["Failed to fetch workflow runs"]

    pr_runs = []
    pr_head_sha = pr_data.get("head", {}).get("sha")

    for run in runs_response.get("workflow_runs", []):
        # Method 1: Check if this run is associated with the PR's head SHA
        if pr_head_sha and run.get("head_sha") == pr_head_sha:
            pr_runs.append(run)
            continue

        # Method 2: Check pull_requests field (may be empty for merged PRs)
        for pr in run.get("pull_requests", []):
            if pr.get("number") == pr_number:
                pr_runs.append(run)
                break

    if not pr_runs:
        # Try alternative approach: get runs by head branch
        pr_head_ref = pr_data.get("head", {}).get("ref")
        if pr_head_ref:
            success, branch_runs = _get_github_api(
                f"actions/runs?branch={pr_head_ref}&per_page=50", headers, owner, repo
            )
            if success:
                pr_runs = branch_runs.get("workflow_runs", [])

    if not pr_runs:
        return False, [
            f"No workflow runs found for PR #{pr_number} (head_sha: {pr_head_sha})"
        ]

    print(f"   Found {len(pr_runs)} workflow run(s) for PR #{pr_number}")

    # Check the most recent run
    latest_run = pr_runs[0]  # GitHub returns runs in descending order by creation time
    run_id = latest_run["id"]

    if latest_run["conclusion"] != "success":
        errors.append(
            f"Latest workflow run {run_id} did not succeed (conclusion: {latest_run['conclusion']})"
        )
    else:
        print(f"   ✅ Latest workflow run {run_id} succeeded")

    # Get jobs for this run
    success, jobs_response = _get_github_api(
        f"actions/runs/{run_id}/jobs", headers, owner, repo
    )

    if not success:
        return False, ["Failed to fetch workflow jobs"]

    jobs = jobs_response.get("jobs", [])
    expected_jobs = [
        "code-quality",
        "testing-suite",
        "security-scan",
        "build-validation",
    ]

    found_jobs = [job["name"] for job in jobs]
    missing_jobs = [job for job in expected_jobs if job not in found_jobs]

    if missing_jobs:
        errors.append(f"Missing jobs: {missing_jobs}. Found: {found_jobs}")
    else:
        print(f"   ✅ All 4 required jobs found: {found_jobs}")

    # Verify all jobs succeeded
    failed_jobs = [job["name"] for job in jobs if job["conclusion"] != "success"]
    if failed_jobs:
        errors.append(f"Failed jobs: {failed_jobs}")
    else:
        print("   ✅ All jobs completed successfully")

    # Verify jobs ran in parallel (started around the same time)
    if len(jobs) >= 4:
        start_times = [job["started_at"] for job in jobs if job["started_at"]]
        if len(start_times) >= 4:
            # Check if all jobs started within 2 minutes of each other
            import datetime

            start_dt = [
                datetime.datetime.fromisoformat(t.replace("Z", "+00:00"))
                for t in start_times
            ]
            time_diff = max(start_dt) - min(start_dt)
            if time_diff.total_seconds() > 120:  # 2 minutes
                errors.append(
                    f"Jobs did not run in parallel (time span: {time_diff.total_seconds()}s)"
                )
            else:
                print("   ✅ Jobs ran in parallel")
        else:
            errors.append("Not enough job start times to verify parallel execution")

    return len(errors) == 0, errors