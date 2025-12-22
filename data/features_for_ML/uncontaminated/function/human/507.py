import time
from datetime import datetime
from typing import Optional, Dict, Any, Union
from curie.docker_setup import ensure_docker_installed

def experiment(api_keys: Optional[Dict[str, str]] = None, 
               dataset_dir: Optional[str] = None, 
               codebase_dir: Optional[str] = None, 
               code_instructions: Optional[str] = None,
               question_file: Optional[str] = None, 
               question: Optional[str] = None, 
               task_config: Optional[Dict[str, Any]] = None, 
               env_requirements: Optional[str] = None,
               max_global_steps: int = 30) -> None:
    """Main experiment function that orchestrates the experiment workflow."""
    # Write API keys to env file if provided
    if api_keys:
        write_api_keys_to_env(api_keys)
    ensure_docker_installed()
    # Load and update configuration
    code_instructions, question_only = split_code_instruction_from_question(codebase_dir, question)
    question = question_only
    task_config = prepare_config(task_config, codebase_dir, dataset_dir, code_instructions, max_global_steps, env_requirements)
    
    print(f"Curie is running with the following configuration: {task_config}")
    
    # Validate question input
    validate_input(question_file, question)
        
    # Prepare question file
    question_file, task_config = prepare_question_file(task_config, question, question_file)
    
    # Run iterations
    iterations = 1
    for iteration in range(1, iterations + 1):
        start_time = time.time()
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        execute_curie(question_file, unique_id, iteration, task_config)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Iteration {iteration} for {question_file} completed in {elapsed_time:.2f} seconds.")