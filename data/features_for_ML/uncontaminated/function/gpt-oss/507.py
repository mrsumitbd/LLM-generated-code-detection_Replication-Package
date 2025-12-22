import os
import sys
import json
import yaml
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def _load_json_or_yaml(file_path: Path) -> Dict[str, Any]:
    with file_path.open("r", encoding="utf-8") as f:
        if file_path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(f) or {}
        return json.load(f)

def _load_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")

def _install_requirements(requirements: str) -> None:
    if not requirements:
        return
    req_file = Path("temp_requirements.txt")
    req_file.write_text(requirements, encoding="utf-8")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
    finally:
        req_file.unlink(missing_ok=True)

def _set_api_keys(api_keys: Dict[str, str]) -> None:
    for key, value in api_keys.items():
        os.environ[key] = value

def _collect_dataset(dataset_dir: Path) -> List[Path]:
    return list(dataset_dir.rglob("*")) if dataset_dir.is_dir() else []

def _collect_codebase(codebase_dir: Path) -> List[Path]:
    return list(codebase_dir.rglob("*.py")) if codebase_dir.is_dir() else []

def _run_step(step_id: int, context: Dict[str, Any]) -> None:
    logging.info(f"Running step {step_id} with context keys: {list(context.keys())}")

def experiment(
    api_keys: Optional[Dict[str, str]] = None,
    dataset_dir: Optional[str] = None,
    codebase_dir: Optional[str] = None,
    code_instructions: Optional[str] = None,
    question_file: Optional[str] = None,
    question: Optional[str] = None,
    task_config: Optional[Dict[str, Any]] = None,
    env_requirements: Optional[str] = None,
    max_global_steps: int = 30,
) -> None:
    """Main experiment function that orchestrates the experiment workflow."""
    # 1. Environment setup
    if env_requirements:
        logging.info("Installing environment requirements")
        _install_requirements(env_requirements)

    if api_keys:
        logging.info("Setting API keys")
        _set_api_keys(api_keys)

    # 2. Load dataset
    dataset_paths: List[Path] = []
    if dataset_dir:
        dataset_dir_path = Path(dataset_dir).expanduser().resolve()
        if dataset_dir_path.is_dir():
            dataset_paths = _collect_dataset(dataset_dir_path)
            logging.info(f"Collected {len(dataset_paths)} dataset files")
        else:
            logging.warning(f"Dataset directory {dataset_dir_path} does not exist")

    # 3. Load codebase
    code_paths: List[Path] = []
    if codebase_dir:
        codebase_path = Path(codebase_dir).expanduser().resolve()
        if codebase_path.is_dir():
            code_paths = _collect_codebase(codebase_path)
            logging.info(f"Collected {len(code_paths)} code files")
        else:
            logging.warning(f"Codebase directory {codebase_path} does not exist")

    # 4. Load question
    question_text: str = ""
    if question_file:
        q_file_path = Path(question_file).expanduser().resolve()
        if q_file_path.is_file():
            question_text = _load_text(q_file_path)
            logging.info(f"Loaded question from {q_file_path}")
        else:
            logging.warning(f"Question file {q_file_path} does not exist")
    elif question:
        question_text = question
        logging.info("Using provided question string")

    # 5. Load task configuration
    task_cfg: Dict[str, Any] = {}
    if task_config:
        task_cfg = task_config
        logging.info("Using provided task configuration")
    else:
        # Attempt to load from a default config file if present
        default_cfg_path = Path("task_config.yaml")
        if default_cfg_path.is_file():
            task_cfg = _load_json_or_yaml(default_cfg_path)
            logging.info(f"Loaded task configuration from {default_cfg_path}")

    # 6. Prepare context for steps
    context: Dict[str, Any] = {
        "dataset_paths": dataset_paths,
        "code_paths": code_paths,
        "question": question_text,
        "task_config": task_cfg,
        "api_keys": api_keys or {},
    }

    # 7. Execute steps
    for step in range(1, max_global_steps + 1):
        try:
            _run_step(step, context)
        except Exception as exc:
            logging.error(f"Error in step {step}: {exc}")
            break

    logging.info("Experiment finished")