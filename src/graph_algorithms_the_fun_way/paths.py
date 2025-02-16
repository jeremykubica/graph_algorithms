"""Functions for operating on paths (Chapter 3).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import math

from typing import Union

from graph_algorithms_the_fun_way.graph import Edge, Graph


# -------------------------------------------------------
# --- Basic Path Metrics --------------------------------
# -------------------------------------------------------


def last_path_length(last: list, final: int, goal: int = -1) -> int:
    """Compute the length of a path defined by a list of previous node indices.

    Parameters
    ----------
    last : list of int
        For each node the index of the node preceding it on the path.
    final : int
        The destination node of the path.
    goal : int
        The origin node of the path.

    Returns
    -------
    count : int
        The path length.
    """
    current: int = final
    count: int = 0

    while current != goal:
        if current == -1:
            return None
        current = last[current]
        count += 1
    return count


def compute_path_cost(g: Graph, path: list) -> float:
    """Compute the cost of a path represented as a list of node indices.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        The node indices on the path.

    Returns
    -------
    cost : float
        The path cost.
    """
    num_nodes: int = len(path)
    if num_nodes == 0:
        return 0.0
    last_node: int = path[0]
    cost: float = 0.0

    step: int = 1
    while step < num_nodes:
        next_node: int = path[step]
        edge: Union[Edge, None] = g.get_edge(last_node, next_node)
        if edge is None:
            return math.inf
        cost = cost + edge.weight
        last_node = next_node
        step = step + 1
    return cost


# -------------------------------------------------------
# --- Basic Path Validity Checks ------------------------
# -------------------------------------------------------


def check_node_path_valid(g: Graph, path: list) -> bool:
    """Check if a path as defined by a list of node indices is valid
    for a given graph.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        The node indices on the path.

    Returns
    -------
    result : bool
        True if the path is valid and False otherwise.
    """
    num_nodes_on_path: int = len(path)
    if num_nodes_on_path == 0:
        return True
    prev_node: int = path[0]
    if prev_node < 0 or prev_node >= g.num_nodes:
        return False

    for step in range(1, num_nodes_on_path):
        next_node: int = path[step]
        if not g.is_edge(prev_node, next_node):
            return False
        prev_node = next_node
    return True


def check_edge_path_valid(g: Graph, path: list) -> bool:
    """Check if a path as defined by a list of Edges is valid
    for a given graph.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of Edge
        The edges along the path.

    Returns
    -------
    result : bool
        True if the path is valid and False otherwise.
    """
    if len(path) == 0:
        return True

    prev_node: int = path[0].from_node
    if prev_node < 0 or prev_node >= g.num_nodes:
        return False

    for edge in path:
        if edge.from_node != prev_node:
            return False

        next_node: int = edge.to_node
        if not g.is_edge(prev_node, next_node):
            return False

        prev_node = next_node
    return True


def check_last_path_valid(g: Graph, last: list) -> bool:
    """Check if a path as defined by a list of previous node indices is valid
    for a given graph.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        For each node the index of the node preceding it on the path.

    Returns
    -------
    result : bool
        True if the path is valid and False otherwise.
    """
    if len(last) != g.num_nodes:
        return False

    for to_node, from_node in enumerate(last):
        if from_node != -1 and not g.is_edge(from_node, to_node):
            return False
    return True


# -------------------------------------------------------
# --- Basic Path Conversions ----------------------------
# -------------------------------------------------------


def edge_path_to_node_path(edge_list: list) -> list:
    """Convert a path represented as a list of edges to a path
    represented as a list of nodes.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of Edge
        The edges along the path.

    Returns
    -------
    result : list of int
        The node indices on the path.
    """
    if len(edge_list) == 0:
        return []

    result: list = [edge_list[0].from_node]
    for edge in edge_list:
        if edge.from_node != result[-1]:
            raise ValueError("Mismatched to and from node.")
        result.append(edge.to_node)

    return result


def node_path_to_edge_path(node_list: list) -> list:
    """Convert a path represented as a list of nodes to a path
    represented as a list of edges.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        The node indices on the path.

    Returns
    -------
    result : list of Edge
        The edges along the path.
    """
    result: list = []
    prev_node: int = -1
    for current in node_list:
        if prev_node != -1:
            result.append(Edge(prev_node, current, 1.0))
        prev_node = current
    return result


def make_node_path_from_last(last: list, dest: int) -> list:
    """Convert a path represented as a list of previous nodes on the path
    to one represented as a list of nodes.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        For each node the index of the node preceding it on the path.

    Returns
    -------
    result : list of int
        The node indices on the path.
    """
    reverse_path: list = []
    current: int = dest

    while current != -1:
        reverse_path.append(current)
        current = last[current]

    path: list = list(reversed(reverse_path))
    return path
