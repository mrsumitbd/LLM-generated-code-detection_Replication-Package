def extract_openai_agents_graph(scan_path: str, output_file: str):
    import os
    import json

    agents = []

    for root, dirs, files in os.walk(scan_path):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    if 'agent' in data:
                        agents.append(data['agent'])

    with open(output_file, 'w') as f:
        json.dump(agents, f)