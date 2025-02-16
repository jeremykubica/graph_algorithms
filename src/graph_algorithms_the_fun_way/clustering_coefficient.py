"""Functions for computing the clustering coefficients (Chapter 2).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from graph_algorithms_the_fun_way.graph import Graph


def clustering_coefficient(g: Graph, ind: int) -> float:
    """Compute the clustering coefficient for a node.

    Parameters
    ----------
    g : Graph
        The input graph.
    ind : int
        The node on which to compute the clustering coefficient.

    Returns
    -------
    result : float
        The clustering coefficient.
    """
    neighbors: set = g.nodes[ind].get_neighbors()
    num_neighbors: int = len(neighbors)

    count: int = 0
    for n1 in neighbors:
        for edge in g.nodes[n1].get_edge_list():
            if edge.to_node > n1 and edge.to_node in neighbors:
                count += 1

    total_possible = (num_neighbors * (num_neighbors - 1)) / 2.0
    if total_possible == 0.0:
        return 0.0
    return count / total_possible


def ave_clustering_coefficient(g: Graph) -> float:
    """Compute the average clustering coefficient for a graph.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    result : float
        The average clustering coefficient.
    """
    total: float = 0.0
    for n in range(g.num_nodes):
        total += clustering_coefficient(g, n)

    if g.num_nodes == 0:
        return 0.0
    return total / g.num_nodes
