import heapq

def _assign_job_to_bucket(
            job_idx: int,
            bucket_idx: int,
            new_workload: float,
        ) -> None:
            # assign the job to this bucket
            self.bucket_partitions[bucket_idx].append(job_idx)
            self.bucket_workloads[bucket_idx] = new_workload
            bucket_nums[bucket_idx] += 1
            # push the updated sum of this bucket back into the heap
            heapq.heappush(heap, (new_workload, bucket_idx))