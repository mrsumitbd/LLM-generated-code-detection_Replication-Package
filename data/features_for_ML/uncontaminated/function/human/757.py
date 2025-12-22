from models import HPCScriptIn, HPCScriptOut, RunIn, RunOut, JobStatusIn, JobStatusOut

def run_simulation_hpc(script_path: str) -> RunOut:
    job_id, ok, err = submit_slurm_job(script_path)
    status = "submitted" if ok else f"failed: {err}"
    return RunOut(job_id=job_id, status=status)