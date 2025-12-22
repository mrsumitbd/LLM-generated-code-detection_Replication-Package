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
    import os
    import json
    from pathlib import Path
    
    # Initialize defaults
    if api_keys is None:
        api_keys = {}
    if task_config is None:
        task_config = {}
    
    # Validate and load question
    if question is None and question_file is None:
        raise ValueError("Either 'question' or 'question_file' must be provided")
    
    if question_file is not None:
        if not os.path.exists(question_file):
            raise FileNotFoundError(f"Question file not found: {question_file}")
        with open(question_file, 'r') as f:
            question = f.read().strip()
    
    if not question:
        raise ValueError("Question cannot be empty")
    
    # Validate directories
    if dataset_dir is not None and not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")
    
    if codebase_dir is not None and not os.path.exists(codebase_dir):
        raise FileNotFoundError(f"Codebase directory not found: {codebase_dir}")
    
    # Load code instructions if provided
    code_context = ""
    if code_instructions is not None:
        if os.path.isfile(code_instructions):
            with open(code_instructions, 'r') as f:
                code_context = f.read()
        else:
            code_context = code_instructions
    
    # Load environment requirements if provided
    env_context = ""
    if env_requirements is not None:
        if os.path.isfile(env_requirements):
            with open(env_requirements, 'r') as f:
                env_context = f.read()
        else:
            env_context = env_requirements
    
    # Build context from codebase if provided
    codebase_context = ""
    if codebase_dir is not None:
        codebase_context = _load_codebase_context(codebase_dir)
    
    # Build context from dataset if provided
    dataset_context = ""
    if dataset_dir is not None:
        dataset_context = _load_dataset_context(dataset_dir)
    
    # Combine all contexts
    full_context = "\n".join(filter(None, [
        code_context,
        env_context,
        codebase_context,
        dataset_context
    ]))
    
    # Execute experiment loop
    step = 0
    while step < max_global_steps:
        step += 1
        
        # Process question with context
        result = _process_step(
            question=question,
            context=full_context,
            api_keys=api_keys,
            task_config=task_config,
            step=step
        )
        
        if result is None or result.get('done', False):
            break
    
    return None


def _load_codebase_context(codebase_dir: str) -> str:
    """Load codebase files as context."""
    import os
    
    context_parts = []
    code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php'}
    
    for root, dirs, files in os.walk(codebase_dir):
        # Skip common non-essential directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}]
        
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        rel_path = os.path.relpath(file_path, codebase_dir)
                        context_parts.append(f"File: {rel_path}\n```\n{content}\n```")
                except Exception:
                    pass
    
    return "\n\n".join(context_parts)


def _load_dataset_context(dataset_dir: str) -> str:
    """Load dataset files as context."""
    import os
    import json
    
    context_parts = []
    data_extensions = {'.json', '.csv', '.txt', '.md', '.yaml', '.yml', '.xml'}
    
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if any(file.endswith(ext) for ext in data_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        rel_path = os.path.relpath(file_path, dataset_dir)
                        context_parts.append(f"Dataset: {rel_path}\n{content}")
                except Exception:
                    pass
    
    return "\n\n".join(context_parts)


def _process_step(question: str, context: str, api_keys: Dict[str, str], 
                  task_config: Dict[str, Any], step: int) -> Optional[Dict[str, Any]]:
    """Process a single step of the experiment."""
    # This is a placeholder for the actual step processing logic
    # In a real implementation, this would interact with an LLM or other service
    return {'done': True}