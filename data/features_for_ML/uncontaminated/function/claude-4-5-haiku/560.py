def verify(max_steps: int, state: AgentState) -> dict:
    """
    ReAct agent for environment verification through test command execution.
    
    Args:
        max_steps (int): Maximum number of verification steps allowed
        state (AgentState): Current agent state with setup results
        
    Returns:
        dict: Updated state with verification results and success status
    """
    import subprocess
    import json
    from typing import Any
    
    # Initialize verification state
    verification_results = []
    step_count = 0
    success = False
    error_message = ""
    
    # Extract setup results from state
    setup_results = state.get("setup_results", {})
    test_commands = state.get("test_commands", [])
    
    if not test_commands:
        test_commands = [
            "python --version",
            "pip list",
        ]
    
    # ReAct loop for verification
    while step_count < max_steps:
        step_count += 1
        
        # Thought: Determine what to verify
        if step_count == 1:
            thought = "Starting environment verification. Will execute test commands to verify setup."
        elif step_count <= len(test_commands):
            thought = f"Executing test command {step_count}: {test_commands[step_count - 1]}"
        else:
            thought = "All test commands executed. Analyzing results."
        
        # Action: Execute test command or analyze
        if step_count <= len(test_commands):
            command = test_commands[step_count - 1]
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                observation = {
                    "command": command,
                    "return_code": result.returncode,
                    "stdout": result.stdout[:500],  # Limit output
                    "stderr": result.stderr[:500],
                    "success": result.returncode == 0
                }
                
                verification_results.append(observation)
                
            except subprocess.TimeoutExpired:
                observation = {
                    "command": command,
                    "error": "Command timeout",
                    "success": False
                }
                verification_results.append(observation)
            except Exception as e:
                observation = {
                    "command": command,
                    "error": str(e),
                    "success": False
                }
                verification_results.append(observation)
        else:
            # Analyze all results
            all_successful = all(
                result.get("success", False) 
                for result in verification_results
            )
            
            if all_successful:
                success = True
                error_message = "All verification tests passed"
            else:
                failed_tests = [
                    r for r in verification_results 
                    if not r.get("success", False)
                ]
                error_message = f"Verification failed: {len(failed_tests)} test(s) failed"
            
            break
    
    # Return updated state
    return {
        "verification_results": verification_results,
        "verification_success": success,
        "verification_error": error_message,
        "verification_steps": step_count,
        "setup_results": setup_results,
        "test_commands": test_commands,
    }