import anthropic
import json
import subprocess
import sys
from pathlib import Path


def profile(repo: str, memory: bool = False, extra_repos: bool = True):
    """
    Profile a repository using Claude to analyze its structure and provide insights.
    
    Args:
        repo: Path to the repository to profile
        memory: Whether to use extended thinking for deeper analysis
        extra_repos: Whether to include analysis of extra repositories
    """
    repo_path = Path(repo)
    if not repo_path.exists():
        print(f"Error: Repository path '{repo}' does not exist")
        sys.exit(1)
    
    client = anthropic.Anthropic()
    
    repo_structure = get_repo_structure(repo_path)
    
    prompt = f"""Analyze the following repository structure and provide insights about the project:

Repository: {repo}
Structure:
{repo_structure}

Please provide:
1. Project Overview: What type of project is this?
2. Key Components: What are the main components/modules?
3. Technology Stack: What technologies are being used?
4. Architecture: How is the project organized?
5. Recommendations: Any suggestions for improvement?"""
    
    if memory:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=16000,
            thinking={
                "type": "enabled",
                "budget_tokens": 10000
            },
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    else:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    print("Repository Profile Analysis")
    print("=" * 50)
    
    for block in response.content:
        if block.type == "thinking":
            print("\n[Extended Thinking Process]")
            print(block.thinking)
            print("-" * 50)
        elif block.type == "text":
            print(block.text)
    
    if extra_repos:
        print("\n" + "=" * 50)
        print("Additional Repository Insights")
        print("=" * 50)
        
        extra_prompt = f"""Based on the repository structure provided earlier, suggest:
1. Related repositories or projects that would complement this one
2. Best practices for this type of project
3. Common pitfalls to avoid"""
        
        extra_response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response.content[0].text if response.content[0].type == "text" else ""},
                {"role": "user", "content": extra_prompt}
            ]
        )
        
        for block in extra_response.content:
            if block.type == "text":
                print(block.text)


def get_repo_structure(repo_path: Path, max_depth: int = 3, current_depth: int = 0, prefix: str = "") -> str:
    """
    Generate a text representation of the repository structure.
    
    Args:
        repo_path: Path to the repository
        max_depth: Maximum depth to traverse
        current_depth: Current depth in traversal
        prefix: Prefix for tree formatting
    
    Returns:
        String representation of the repository structure
    """
    if current_depth >= max_depth:
        return ""
    
    structure = ""
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', '.egg-info', 'dist', 'build'}
    ignore_files = {'.pyc', '.pyo', '.pyd', '.so', '.dll'}
    
    try:
        items = sorted(repo_path.iterdir())
    except PermissionError:
        return ""
    
    dirs = []
    files = []
    
    for item in items:
        if item.name.startswith('.') and item.name not in {'.github', '.gitignore'}:
            continue
        if item.name in ignore_dirs:
            continue
        if item.is_dir():
            dirs.append(item)
        else:
            if not any(item.name.endswith(ext) for ext in ignore_files):
                files.append(item)
    
    for file in files[:10]:
        structure += f"{prefix}├── {file.name}\n"
    
    if len(files) > 10:
        structure += f"{prefix}├── ... ({len(files) - 10} more files)\n"
    
    for i, dir_item in enumerate(dirs[:5]):
        is_last = (i == len(dirs) - 1) and len(dirs) <= 5
        structure += f"{prefix}├── {dir_item.name}/\n"
        
        sub_prefix = prefix + ("    " if is_last else "│   ")
        sub_structure = get_repo_structure(dir_item, max_depth, current_depth + 1, sub_prefix)
        structure += sub_structure
    
    if len(dirs) > 5:
        structure += f"{prefix}├── ... ({len(dirs) - 5} more directories)\n"
    
    return structure


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Profile a repository using Claude")
    parser.add_argument("repo", help="Path to the repository to profile")
    parser.add_argument("--memory", action="store_true", help="Use extended thinking for deeper analysis")
    parser.add_argument("--no-extra", action="store_true", help="Skip extra repository insights")
    
    args = parser.parse_args()
    
    profile(args.repo, memory=args.memory, extra_repos=not args.no_extra)