from locust.runners import LocalRunner, MasterRunner, WorkerRunner
import time
from locust.runners import WorkerRunner
import signal
import os

def graceful_signal_handler(signum, frame):
    """
    Custom signal handler to gracefully handle SIGTERM when Locust is already shutting down.
    This prevents the "stopping state" exception from being raised.
    """
    global _shutdown_in_progress
    if _shutdown_in_progress:
        return
    task_id = os.environ.get("TASK_ID", "unknown")
    task_logger = global_state.get_task_logger(task_id)
    _shutdown_in_progress = True

    try:
        # Ensure Worker process sends stats before exiting
        if hasattr(frame, "f_globals") and "environment" in frame.f_globals:
            env = frame.f_globals["environment"]
            try:
                from locust.runners import WorkerRunner

                is_worker = hasattr(env, "runner") and isinstance(
                    env.runner, WorkerRunner
                )
            except ImportError:
                is_worker = hasattr(env, "runner") and "WorkerRunner" in str(
                    type(env.runner)
                )

            if is_worker:
                task_logger.debug(
                    f"Worker process {os.getpid()} received signal {signum}, ensuring metrics are sent..."
                )
                try:
                    # Send emergency stats
                    stats_manager.send_stats_to_master(
                        env.runner,
                        reqs=0,  # Do not increment request count
                        completion_tokens=0,
                        total_tokens=0,
                    )
                    time.sleep(0.5)
                except Exception as e:
                    task_logger.error(f"Failed to send emergency metrics: {e}")
    except Exception as e:
        task_logger.warning(f"Error in graceful signal handler: {e}")

    # Restore default signal handler
    signal.signal(signum, signal.SIG_DFL)
    os.kill(os.getpid(), signum)