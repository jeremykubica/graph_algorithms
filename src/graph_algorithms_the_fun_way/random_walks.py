"""Algorithms for the random walk functions in chapter 13.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import random

from graph_algorithms_the_fun_way.graph import Graph, Node


def is_valid_probability_graph(g: Graph) -> bool:
    """Check if a graph's edges represent a valid probability distributions.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    bool
        Whether the graph is a valid probability graph.
    """
    for node in g.nodes:
        edge_list: list = node.get_edge_list()
        if len(edge_list) == 0:
            return False

        total: float = 0.0
        for edge in edge_list:
            if edge.weight < 0.0 or edge.weight > 1.0:
                return False
            total += edge.weight
        if abs(total - 1.0) > 1e-10:
            return False

    return True


def choose_next_node(current: Node) -> int:
    """Randomly choose a neighboring node to which to transition.

    Parameters
    ----------
    current : Node
        The current node.

    Returns
    -------
    int
        The index of the choosen neighbor.
    """
    prob: float = random.random()
    cumulative: float = 0.0
    edge_list: list = current.get_edge_list()

    for edge in edge_list:
        cumulative += edge.weight
        if cumulative >= prob:
            return edge.to_node
    return edge_list[-1].to_node


def choose_start(S: list) -> int:
    """Randomly choose a starting node for a walk.

    Parameters
    ----------
    S : list of float
        Maps each node's index to the probability that it is choosen.

    Returns
    -------
    int
        The index of the choosen starting node.
    """
    prob: float = random.random()
    cumulative: float = 0.0

    for i in range(len(S)):
        cumulative += S[i]
        if cumulative >= prob:
            return i
    return len(S) - 1


def random_walk(g: Graph, start: int, steps: int) -> list:
    """Perform a random walk on a graph.

    Parameters
    ----------
    g : Graph
        The input graph.
    start : int
        The index of the starting node.
    steps : int
        The number of steps to take.

    Returns
    -------
    walk : list
        The nodes visited (in order).
    """
    if not is_valid_probability_graph(g):
        raise ValueError("Graph weights are not probabilities.")

    walk: list = [-1] * steps
    current: int = start
    walk[0] = current
    for i in range(1, steps):
        current = choose_next_node(g.nodes[current])
        walk[i] = current
    return walk


def estimate_graph_from_random_walks(walks: list) -> Graph:
    """Estimate the underlying probability graph from a list of walks.

    Parameters
    ----------
    walks : list of list of int
        A list of walks.

    Returns
    -------
    g : Graph
        The estimated probability graph.
    """
    num_nodes: int = 0
    for path in walks:
        for node in path:
            if node >= num_nodes:
                num_nodes = node + 1

    counts: list = [0.0] * num_nodes
    move_counts: list = [[0.0] * num_nodes for _ in range(num_nodes)]
    for path in walks:
        for i in range(0, len(path) - 1):
            counts[path[i]] += 1.0
            move_counts[path[i]][path[i + 1]] += 1.0

    g: Graph = Graph(num_nodes)
    for i in range(num_nodes):
        if counts[i] > 0.0:
            for j in range(num_nodes):
                if move_counts[i][j] > 0.0:
                    g.insert_edge(i, j, move_counts[i][j] / counts[i])
    return g


def estimate_start_from_random_walks(walks: list) -> list:
    """Estimate the underlying starting probabilities from a list of walks.

    Parameters
    ----------
    walks : list of list of int
        A list of walks.

    Returns
    -------
    counts : list of floats
        Maps each node's index to the probability that it is choosen.
    """
    num_nodes: int = 0
    for path in walks:
        for node in path:
            if node >= num_nodes:
                num_nodes = node + 1
    counts: list = [0.0] * num_nodes

    for path in walks:
        counts[path[0]] += 1.0

    for i in range(num_nodes):
        counts[i] = counts[i] / len(walks)
    return counts
