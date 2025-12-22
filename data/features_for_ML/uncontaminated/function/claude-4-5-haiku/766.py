def process_instance(
    instance: dict,
    output_dir: Path,
    config: dict,
    progress_manager: RunBatchProgressManager,
) -> None:
    """Process a single SWEBench instance."""
    instance_id = instance.get("instance_id")
    if not instance_id:
        progress_manager.log_error("Instance missing instance_id")
        return
    
    instance_output_dir = output_dir / instance_id
    instance_output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Save instance metadata
        metadata_file = instance_output_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(instance, f, indent=2)
        
        # Extract repository information
        repo_name = instance.get("repo")
        base_commit = instance.get("base_commit")
        test_patch = instance.get("test_patch")
        problem_statement = instance.get("problem_statement")
        
        if not all([repo_name, base_commit]):
            progress_manager.log_error(f"Instance {instance_id} missing repo or base_commit")
            return
        
        # Setup repository
        repo_dir = instance_output_dir / "repo"
        repo_dir.mkdir(exist_ok=True)
        
        # Clone or setup repository
        setup_repo(repo_dir, repo_name, base_commit, config)
        
        # Apply test patch if provided
        if test_patch:
            apply_patch(repo_dir, test_patch)
        
        # Run tests
        test_results = run_tests(repo_dir, instance, config)
        
        # Save test results
        results_file = instance_output_dir / "test_results.json"
        with open(results_file, "w") as f:
            json.dump(test_results, f, indent=2)
        
        # Log success
        progress_manager.log_success(instance_id)
        
    except Exception as e:
        progress_manager.log_error(f"Error processing instance {instance_id}: {str(e)}")
        raise


def setup_repo(repo_dir: Path, repo_name: str, base_commit: str, config: dict) -> None:
    """Setup repository at specified commit."""
    if not (repo_dir / ".git").exists():
        subprocess.run(
            ["git", "clone", f"https://github.com/{repo_name}.git", str(repo_dir)],
            check=True,
            capture_output=True
        )
    
    subprocess.run(
        ["git", "checkout", base_commit],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )


def apply_patch(repo_dir: Path, patch_content: str) -> None:
    """Apply a patch to the repository."""
    patch_file = repo_dir / "temp.patch"
    with open(patch_file, "w") as f:
        f.write(patch_content)
    
    subprocess.run(
        ["git", "apply", str(patch_file)],
        cwd=repo_dir,
        check=True,
        capture_output=True
    )
    
    patch_file.unlink()


def run_tests(repo_dir: Path, instance: dict, config: dict) -> dict:
    """Run tests for the instance."""
    test_command = instance.get("test_command")
    if not test_command:
        return {"status": "skipped", "reason": "No test command provided"}
    
    try:
        result = subprocess.run(
            test_command,
            cwd=repo_dir,
            shell=True,
            capture_output=True,
            text=True,
            timeout=config.get("test_timeout", 300)
        )
        
        return {
            "status": "completed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "passed": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "passed": False}
    except Exception as e:
        return {"status": "error", "error": str(e), "passed": False}