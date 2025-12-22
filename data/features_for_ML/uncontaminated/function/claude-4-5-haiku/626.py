def _assign_job_to_bucket(
            job_idx: int,
            bucket_idx: int,
            new_workload: float,
        ) -> None:
            # assign the job to this bucket
            jobs[job_idx] = bucket_idx
            buckets[bucket_idx] += new_workload