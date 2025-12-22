from pathlib import Path
import json
import os
import sys

def extract_openai_agents_graph(scan_path: str, output_file: str):
    existing_tools_file = "existing_tools.json" # Hardcoded path

    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.")
        sys.exit(1)


    print(f"Analyzing agent structures in: {scan_path}")

    try:
        custom_tools, custom_locs = gather_tool_definitions(scan_path)
        existing_tools = load_existing_tool_defs(existing_tools_file)
        available_tools = {**existing_tools, **custom_tools}
        print(f"Total available tools: {len(available_tools)}")

        agents, var_agent_link = gather_agent_definitions(scan_path, available_tools)

        start_points = find_execution_starts(scan_path)
        print(f"Found {len(start_points)} potential execution starts.")

        final_graph = build_graph_json(
            agents=agents,
            custom_tools=custom_tools,
            custom_tool_locs=custom_locs,
            existing_tools=existing_tools,
            start_points=start_points,
            var_agent_link=var_agent_link
        )
        print(f"Analysis complete. Nodes: {len(final_graph['nodes'])}, Edges: {len(final_graph['edges'])}.")

        if final_graph:
            final_graph["metadata"] = {
                "framework": "OpenAI_Agents",
            }

    except Exception as e:
         print(f"Error during graph extraction: {e}")
         sys.exit(1)


    if final_graph["nodes"] or final_graph["edges"]:
        try:

            final_graph["nodes"].sort(key=lambda x: x.get('id', ''))
            final_graph["edges"].sort(key=lambda x: (x.get('source', ''), x.get('target', ''), x.get('edge_type', '')))


            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding='utf-8') as f:
                json.dump(final_graph, f, indent=2)
            print(f"\nGraph structure written to {output_path}")


            print("\n--- Summary ---")
            if not final_graph["nodes"]: print("No nodes found.")
            for node in final_graph["nodes"]:
                 loc = node.get('source_location')
                 loc_str = f" ({loc['file']}:{loc['line']})" if loc and loc.get('file') else ""
                 node_id = node.get('id', 'Unknown ID')
                 node_type = node.get('node_type', 'Unknown Type')
                 print(f"Node: {node_id} ({node_type}){loc_str}")

            if not final_graph["edges"]: print("No edges found.")
            for edge in final_graph["edges"]:
                 cond_str = f" Cond: {edge.get('condition')}" if edge.get('condition') else ""
                 meta_loc = edge.get('metadata', {}).get('definition_location')
                 loc_str = f" ({meta_loc['file']}:{meta_loc['line']})" if meta_loc and meta_loc.get('file') else ""
                 source = edge.get('source', 'Unknown')
                 target = edge.get('target', 'Unknown')
                 edge_type = edge.get('edge_type', 'Unknown Type')
                 print(f"Edge: {source} -> {target} ({edge_type}){cond_str}{loc_str}")

        except Exception as e:
            print(f"Error writing JSON output or printing summary: {e}")
            sys.exit(1)
    else:
        print("\nNo graph structure found or extracted.")
        try:

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding='utf-8') as f:
                json.dump({"nodes": [], "edges": []}, f, indent=2)
            print(f"Empty graph structure written to {output_path}")
        except Exception as e:
            print(f"Error writing empty JSON output to {output_path}: {e}")
            sys.exit(1)