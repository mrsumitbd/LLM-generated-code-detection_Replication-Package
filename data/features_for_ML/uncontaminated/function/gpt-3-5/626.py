def _assign_job_to_bucket(
    job_idx: int,
    bucket_idx: int,
    new_workload: float,
) -> None:
    # assign the job to this bucket
    print(f"Assigned job {job_idx} to bucket {bucket_idx} with new workload {new_workload}")