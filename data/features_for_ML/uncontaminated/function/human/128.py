def parse_all_graph_instances_in_directory(
    root_directory,
    graph_class_fqcn,
    command_class_fqn,
    add_conditional_edges_method_name,
    add_node_method_name,
    global_functions,
    global_variables,
):
    results = walk_directory_and_parse(
        root_directory,
        graph_class_fqcn,
        command_class_fqn,
        add_conditional_edges_method_name,
        add_node_method_name,
        global_functions,
        global_variables,
    )
    graphs = []
    for graph, call_records in results.items():
        nodes = []
        basic_edges = []
        conditional_edges = []

        if call_records.get("add_node", False):
            call_data = call_records.get("add_node")
            for single_call in call_data:
                # The actual name if the method received 2 arguments, and the name of the function if it received one
                node_name = single_call["positional"][0]
                node_definition = single_call["node_definition_argument_info"]
                nodes.append({"name": node_name, "definition": node_definition})

            # Resolving the goto arguments of the Command objects
            for single_call in call_data:
                node_name = single_call["positional"][0]
                all_node_names = [node["name"] for node in nodes] + ["START", "END"]
                resolved_gotos = [
                    goto for goto in single_call["gotos"] if goto in all_node_names
                ]

                if len(resolved_gotos) > 1:
                    for resolved_goto in resolved_gotos:
                        conditional_edges.append(
                            {
                                "resolved": True,
                                "start_node": node_name,
                                "end_node": resolved_goto,
                            }
                        )
                elif len(resolved_gotos) == 1:
                    basic_edges.append(
                        {"start_node": node_name, "end_node": resolved_gotos[0]}
                    )

        if call_records.get("add_edge", False):
            all_node_names = [node["name"] for node in nodes] + ["START", "END"]
            call_data = call_records.get("add_edge")
            for single_call in call_data:
                nodes_in_edge = []
                # Since the call always contains two node names, we just add names from positional and keyword arguments (in this exact order)
                for node_name in single_call["positional"]:
                    nodes_in_edge.append(node_name)
                for _, node_name in single_call["keyword"].items():
                    nodes_in_edge.append(node_name)

                if (
                    nodes_in_edge[0] in all_node_names
                    and nodes_in_edge[1] in all_node_names
                ):
                    basic_edges.append(
                        {"start_node": nodes_in_edge[0], "end_node": nodes_in_edge[1]}
                    )

        if call_records.get("add_conditional_edges", False):
            all_node_names = [node["name"] for node in nodes] + ["START", "END"]
            call_data = call_records.get("add_conditional_edges")
            for single_call in call_data:
                # Resolving arguments to find the source node
                arguments = []
                for argument in single_call["positional"]:
                    arguments.append(argument)
                for _, argument in single_call["keyword"].items():
                    arguments.append(argument)

                if single_call.get("path", False):
                    if single_call["path"].get("function_returns", False):
                        for end_node in single_call["path"].get("function_returns"):
                            if (
                                arguments[0] in all_node_names
                                and end_node in all_node_names
                            ):
                                conditional_edges.append(
                                    {
                                        "resolved": True,
                                        "start_node": arguments[0],
                                        "end_node": end_node,
                                    }
                                )
                elif single_call.get("path_map", False):
                    if single_call["path_map"].get("list_values", False):
                        for end_node in single_call["path_map"].get("list_values"):
                            if (
                                arguments[0] in all_node_names
                                and end_node in all_node_names
                            ):
                                conditional_edges.append(
                                    {
                                        "resolved": True,
                                        "start_node": arguments[0],
                                        "end_node": end_node,
                                    }
                                )
                    elif single_call["path_map"].get("dict_values", False):
                        for end_node in single_call["path_map"].get("dict_values"):
                            if (
                                arguments[0] in all_node_names
                                and end_node in all_node_names
                            ):
                                conditional_edges.append(
                                    {
                                        "resolved": True,
                                        "start_node": arguments[0],
                                        "end_node": end_node,
                                    }
                                )
        if call_records.get("set_entry_point", False):
            call_data = call_records.get("set_entry_point")
            entrypoints = []
            for single_call in call_data:
                for node_name in single_call["positional"]:
                    entrypoints.append(node_name)
                for _, node_name in single_call["keyword"].items():
                    entrypoints.append(node_name)

            for node_name in entrypoints:
                basic_edges.append({"start_node": "START", "end_node": node_name})
        graphs.append(
            {
                "graph_name": graph,
                "graph_info": {
                    "nodes": nodes,
                    "basic_edges": basic_edges,
                    "conditional_edges": conditional_edges,
                },
            }
        )
    return graphs