import matplotlib.pyplot as plt
import networkx as nx
import csv
import os
import json


def save_results(output_path, community, community_patterns):
    row = [
        community.repo_owner,
        community.repo_name,
        community.data.start_date,
        community.data.end_date,
    ]
    for key in community_patterns:
        row.append(community_patterns[key])
    with open(output_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(row)
    data_path = os.path.join("data", community.repo_owner, community.repo_name)
    if not os.path.exists(data_path):
        # if the data directory is not present
        # then create it.
        os.makedirs(data_path)
    """    
    with open(
        os.path.join(data_path, "data.json"),
        "w",
    ) as f:
        json.dump(community.data.__dict__, f)"""
    with open(
        os.path.join(data_path, "metrics.json"),
        "w",
    ) as f:
        json.dump(community.metrics.__dict__, f)


def print_graph(G, community):
    graphs = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    for i in range(len(graphs)):
        # positions for all nodes - seed for reproducibility
        pos = nx.spring_layout(graphs[i], seed=7)

        # nodes
        nx.draw_networkx_nodes(graphs[i], pos, node_size=500)

        # edges
        nx.draw_networkx_edges(
            graphs[i], pos, edgelist=graphs[i].edges, width=2, edge_color="b"
        )

        # node labels
        nx.draw_networkx_labels(graphs[i], pos, font_size=12, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(graphs[i], "weight")
        nx.draw_networkx_edge_labels(graphs[i], pos, edge_labels)

        ax = plt.gca()
        plt.axis("off")
        filname = (
            community.repo_owner
            + "-"
            + community.repo_name
            + "_graph"
            + str(i)
            + ".png"
        )
        graphs_path = os.path.join("graphs", community.repo_owner, community.repo_name)
        if not os.path.exists(graphs_path):
            # if the graphs directory is not present
            # then create it.
            os.makedirs(graphs_path)

        plt.savefig(
            os.path.join(graphs_path, filname),
            format="PNG",
        )
        nx.write_gexf(G, os.path.join(graphs_path, filname + ".gexf"))
