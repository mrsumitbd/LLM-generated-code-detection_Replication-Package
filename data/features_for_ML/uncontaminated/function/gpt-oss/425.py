import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional


def _run_command(cmd: list[str], cwd: Path, capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the CompletedProcess."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=False,
    )


def _install_dependencies(repo_path: Path) -> None:
    """Install the repository in editable mode and its requirements if present."""
    # Editable install
    _run_command([sys.executable, "-m", "pip", "install", "-e", "."], cwd=repo_path)
    # Install requirements.txt if exists
    req_file = repo_path / "requirements.txt"
    if req_file.is_file():
        _run_command([sys.executable, "-m", "pip", "install", "-r", str(req_file)], cwd=repo_path)


def _run_tests_with_coverage(repo_path: Path, memory: bool) -> Dict[str, Any]:
    """Run pytest with coverage and optionally memory profiling."""
    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=.",
        "--cov-report=json",
        "--cov-report=term-missing",
    ]

    if memory:
        # Use memory_profiler's mprof if available
        mprof_path = shutil.which("mprof")
        if mprof_path:
            pytest_cmd = [mprof_path, "run"] + pytest_cmd

    result = _run_command(pytest_cmd, cwd=repo_path)

    # Parse coverage JSON
    cov_json = repo_path / ".coverage.json"
    coverage_percent: Optional[float] = None
    if cov_json.is_file():
        try:
            with cov_json.open() as f:
                cov_data = json.load(f)
                coverage_percent = cov_data.get("totals", {}).get("percent_covered", None)
        except Exception:
            coverage_percent = None

    # Parse memory profile if mprof was used
    memory_profile: Optional[str] = None
    if memory:
        mprof_png = repo_path / "mprof.png"
        if mprof_png.is_file():
            memory_profile = str(mprof_png)

    return {
        "tests_passed": result.returncode == 0,
        "coverage_percent": coverage_percent,
        "memory_profile": memory_profile,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def profile(repo: str, memory: bool = False, extra_repos: bool = True) -> Dict[str, Any]:
    """
    Profile a Python repository.

    Parameters
    ----------
    repo : str
        Path to the repository to profile.
    memory : bool, optional
        If True, run memory profiling using mprof.
    extra_repos : bool, optional
        If True, install dependencies from requirements.txt if present.

    Returns
    -------
    dict
        Dictionary containing profiling results:
        - tests_passed (bool)
        - coverage_percent (float or None)
        - memory_profile (str or None)
        - stdout (str)
        - stderr (str)
    """
    repo_path = Path(repo).expanduser().resolve()
    if not repo_path.is_dir():
        raise FileNotFoundError(f"Repository path '{repo}' does not exist or is not a directory.")

    # Install dependencies if requested
    if extra_repos:
        _install_dependencies(repo_path)

    # Run tests with coverage (and memory profiling if requested)
    results = _run_tests_with_coverage(repo_path, memory)

    return results