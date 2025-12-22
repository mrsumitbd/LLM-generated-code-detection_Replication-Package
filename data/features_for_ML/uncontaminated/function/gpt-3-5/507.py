def experiment(api_keys=None, dataset_dir=None, codebase_dir=None, code_instructions=None,
               question_file=None, question=None, task_config=None, env_requirements=None,
               max_global_steps=30):
    
    print("Running experiment with the following parameters:")
    print(f"api_keys: {api_keys}")
    print(f"dataset_dir: {dataset_dir}")
    print(f"codebase_dir: {codebase_dir}")
    print(f"code_instructions: {code_instructions}")
    print(f"question_file: {question_file}")
    print(f"question: {question}")
    print(f"task_config: {task_config}")
    print(f"env_requirements: {env_requirements}")
    print(f"max_global_steps: {max_global_steps}")