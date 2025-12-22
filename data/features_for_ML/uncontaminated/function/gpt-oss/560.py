from typing import Any, Dict, List

def verify(max_steps: int, state: Any) -> Dict[str, Any]:
    """
    ReAct agent for environment verification through test command execution.

    Args:
        max_steps (int): Maximum number of verification steps allowed
        state (AgentState): Current agent state with setup results

    Returns:
        dict: Updated state with verification results and success status
    """
    # Prepare containers for results
    verification_results: List[Dict[str, Any]] = []
    success = True
    steps_taken = 0

    # Helper to get attribute safely
    def _get(attr: str, default=None):
        return getattr(state, attr, default)

    # Retrieve pending tests; assume a list of command strings
    pending_tests: List[str] = _get("pending_tests", [])
    # Retrieve a method to run a test; fallback to a simple exec if not provided
    run_test = _get("run_test")

    # If no run_test method, define a simple placeholder
    if run_test is None:
        def run_test(cmd: str) -> Dict[str, Any]:
            try:
                # Execute the command in a subprocess and capture output
                import subprocess, shlex
                result = subprocess.run(
                    shlex.split(cmd),
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return {
                    "command": cmd,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "success": result.returncode == 0,
                }
            except Exception as e:
                return {
                    "command": cmd,
                    "error": str(e),
                    "success": False,
                }

    # Main verification loop
    for cmd in pending_tests[:max_steps]:
        steps_taken += 1
        result = run_test(cmd)
        verification_results.append(result)
        if not result.get("success", False):
            success = False
            break

    # Update state with results
    if hasattr(state, "verification_results"):
        setattr(state, "verification_results", verification_results)
    else:
        state.verification_results = verification_results

    if hasattr(state, "verification_success"):
        setattr(state, "verification_success", success)
    else:
        state.verification_success = success

    if hasattr(state, "verification_steps"):
        setattr(state, "verification_steps", steps_taken)
    else:
        state.verification_steps = steps_taken

    # Return a dictionary representation of the updated state
    return {
        "verification_results": verification_results,
        "verification_success": success,
        "verification_steps": steps_taken,
    }