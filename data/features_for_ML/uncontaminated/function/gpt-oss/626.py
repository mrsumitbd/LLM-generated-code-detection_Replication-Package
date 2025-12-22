def _assign_job_to_bucket(
    job_idx: int,
    bucket_idx: int,
    new_workload: float,
) -> None:
    """
    Assign a job to a bucket, updating the global bookkeeping structures.

    The function assumes the following global mutable structures exist:
        - `job_to_bucket`: a list (or dict) mapping job indices to the index of the bucket
          that currently holds the job.  A value of ``None`` indicates that the job is
          not assigned to any bucket.
        - `bucket_workloads`: a list (or dict) holding the current workload of each
          bucket.  The workload of the target bucket is replaced with ``new_workload``.
        - `bucket_jobs`: a list (or dict) of collections (lists or sets) that contain
          the job indices assigned to each bucket.

    The function removes the job from its previous bucket (if any), adds it to the
    new bucket, updates the mapping, and sets the new workload for the target bucket.
    """
    # Retrieve the global bookkeeping structures
    global job_to_bucket, bucket_workloads, bucket_jobs

    # Determine the previous bucket of the job (if any)
    old_bucket = job_to_bucket[job_idx] if job_idx in job_to_bucket else None

    # If the job was already in the target bucket, nothing to do
    if old_bucket == bucket_idx:
        job_to_bucket[job_idx] = bucket_idx
        bucket_workloads[bucket_idx] = new_workload
        return

    # Remove the job from its old bucket, if it was assigned
    if old_bucket is not None:
        # Use the appropriate removal method depending on the container type
        try:
            bucket_jobs[old_bucket].remove(job_idx)
        except (AttributeError, ValueError):
            # If the container is a set, use discard
            try:
                bucket_jobs[old_bucket].discard(job_idx)
            except AttributeError:
                # If removal fails, ignore – the job might not be present
                pass

    # Add the job to the new bucket
    try:
        bucket_jobs[bucket_idx].append(job_idx)
    except AttributeError:
        # If the container is a set, use add
        try:
            bucket_jobs[bucket_idx].add(job_idx)
        except AttributeError:
            # If the container is neither list nor set, create a new list
            bucket_jobs[bucket_idx] = [job_idx]

    # Update the mapping and workload
    job_to_bucket[job_idx] = bucket_idx
    bucket_workloads[bucket_idx] = new_workload