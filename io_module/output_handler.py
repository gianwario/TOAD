import matplotlib.pyplot as plt
import networkx as nx
import csv


def save_results(output_path, community, commmunity_patterns):
    row = [
        community.repo_owner,
        community.repo_name,
        community.data.start_date,
        community.data.end_date,
    ]
    for key in commmunity_patterns:
        row.append(commmunity_patterns[key])
    with open(output_path, "a") as file:
        writer = csv.writer(file)
        writer.writerow(row)

    """
        dict = {
        "owner": community.repo_owner,
        "name": community.repo_name,
        "start_date": community.data.start_date,
        "end_date": community.data.end_date,
        "SN": None,
        "NoP": None,
        "IN": None,
        "FN": None,
        "CoP": None,
        "PT": None,
        "FG": None,
        "IC": None,
    }
    for key in commmunity_patterns:
        dict[key] = commmunity_patterns[key]
    with open(output_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(row)
    with open('demo_csv.csv', 'a') as csv_file:
        dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
    
        dict_object.writerow(dict)
    """


def print_graph(G, commmunity):
    # positions for all nodes - seed for reproducibility
    pos = nx.spring_layout(G, seed=7)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=6, edge_color="b")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    filname = commmunity.repo_owner + "-" + commmunity.repo_name + "_graph.png"
    plt.savefig(filname, format="PNG")
