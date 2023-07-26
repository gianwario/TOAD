from community import community
import networkx as nx
from io_module import output_handler
from console import console
from utils import intersection


def compute_structure_data(community: community.Community):
    G = nx.Graph()
    G.add_nodes_from(community.data.members_logins)

    repo_connections = compute_common_projects_connection(community, G)
    follow_connections = compute_follows_connection(community, G)
    output_handler.print_graph(G)
    pass


def compute_common_projects_connection(community: community.Community, G: nx.Graph):
    """
    This method computes the common projects connections between all couple of users, adding an edge if one common repository
    exists and giving the edge a weight equal to the number of common projects
    """
    connections = {}
    mapping = community.data.map_user_repositories
    for member in mapping:
        connections[member] = []
        for other_member in mapping:
            if member != other_member:
                common_projects = intersection(mapping[member], mapping[other_member])
                connections[member].append({other_member: len(common_projects)})
                if len(common_projects) > 0:
                    G.add_edge(member, other_member, weight=len(common_projects))
    return connections


def compute_follows_connection(community: community.Community, G: nx.Graph):
    """
    This method computes the following/follower relationship between 2 users, adding an edge if one of is true
    and giving more weight if both follow each other (i.e. edge with weight 1 if only x follows y or edge with
    weight 2 if both x follows y and y follows x)
    """
    connections = {}
    mapping_follower = community.data.map_user_followers
    mapping_following = community.data.map_user_following
    for member in community.data.members_logins:
        connections[member] = []
        for other_member in mapping_follower[member]:
            if (
                other_member in mapping_following
                and member in mapping_following[other_member]
            ):
                connections[member].append(other_member)
                if G.has_edge(member, other_member):
                    G.add_edge(
                        member,
                        other_member,
                        weight=G[member][other_member]["weight"] + 1,
                    )
                else:
                    G.add_edge(member, other_member, weight=1)
    return connections
