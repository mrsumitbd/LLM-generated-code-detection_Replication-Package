import os
import networkx as nx
import matplotlib.pyplot as plt

def extract_openai_agents_graph(scan_path: str, output_file: str):
    # Create a directed graph
    G = nx.DiGraph()

    # Iterate through the files in the scan_path directory
    for filename in os.listdir(scan_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(scan_path, filename)
            with open(filepath, "r") as file:
                # Read the contents of the file
                content = file.read()

            # Split the content into lines
            lines = content.strip().split("\n")

            # Extract the agent names from the lines
            agents = [line.split(":")[0] for line in lines]

            # Add the agents as nodes to the graph
            for agent in agents:
                G.add_node(agent)

            # Create edges between the agents based on the order in the file
            for i in range(len(agents) - 1):
                G.add_edge(agents[i], agents[i + 1])

    # Save the graph to the output file
    nx.write_gexf(G, output_file)

    # Visualize the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.savefig(output_file.replace(".gexf", ".png"))