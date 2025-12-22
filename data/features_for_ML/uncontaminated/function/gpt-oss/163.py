import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set

def _load_agent_file(path: Path) -> Dict:
    """Load a JSON or YAML file and return its content as a dict."""
    try:
        with path.open("r", encoding="utf-8") as f:
            if path.suffix.lower() in {".json"}:
                return json.load(f)
            else:
                return yaml.safe_load(f) or {}
    except Exception:
        return {}

def _extract_agent_info(data: Dict) -> (str, List[str]):
    """
    Extract agent name and list of called agents from the data dict.
    The function looks for common keys: 'name', 'agent_name', 'calls', 'called_agents'.
    """
    name = data.get("name") or data.get("agent_name") or data.get("id") or ""
    calls = data.get("calls") or data.get("called_agents") or data.get("calls_to") or []
    if isinstance(calls, str):
        calls = [calls]
    if isinstance(calls, list):
        calls = [str(c).strip() for c in calls if c]
    return name.strip(), calls

def extract_openai_agents_graph(scan_path: str, output_file: str):
    """
    Scan the directory `scan_path` for JSON/YAML files that define OpenAI agents,
    build a directed graph of agent interactions, and write the graph to
    `output_file` as a JSON adjacency list.

    The graph is represented as:
        {
            "agent_name": ["called_agent_1", "called_agent_2", ...],
            ...
        }

    Parameters
    ----------
    scan_path : str
        Path to the directory to scan for agent definition files.
    output_file : str
        Path to the output file where the graph JSON will be written.
    """
    scan_dir = Path(scan_path)
    if not scan_dir.is_dir():
        raise ValueError(f"Scan path '{scan_path}' is not a directory")

    graph: Dict[str, Set[str]] = {}
    # Keep track of all discovered agent names
    all_agents: Set[str] = set()

    # Walk through the directory recursively
    for root, _, files in os.walk(scan_dir):
        for filename in files:
            file_path = Path(root) / filename
            if file_path.suffix.lower() not in {".json", ".yaml", ".yml"}:
                continue
            data = _load_agent_file(file_path)
            if not isinstance(data, dict):
                continue
            name, calls = _extract_agent_info(data)
            if not name:
                continue
            all_agents.add(name)
            graph.setdefault(name, set()).update(calls)

    # Ensure all called agents are present as nodes (even if they have no definition)
    for calls in graph.values():
        for callee in calls:
            all_agents.add(callee)
            graph.setdefault(callee, set())

    # Convert sets to sorted lists for deterministic output
    adjacency: Dict[str, List[str]] = {
        node: sorted(list(neighbors)) for node, neighbors in graph.items()
    }

    # Write to output file
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(adjacency, f, indent=2, sort_keys=True)