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
from graph_algorithms_the_fun_way.search import dfs_connected_components


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


# -------------------------------------------------------
# --- Functions for Hamiltonian Paths -------------------
# -------------------------------------------------------


def is_hamiltonian_path(g: Graph, path: list) -> bool:
    """Checks whether a path is a valid Hamiltonian cycle.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        For each node the index of the node preceding it on the path.

    Returns
    -------
    result : bool
        True if the path is a Hamiltonian cycle and False otherwise.
    """
    num_nodes: int = len(path)
    if num_nodes != g.num_nodes:
        return False

    visited: list = [False] * g.num_nodes
    prev_node: int = path[0]
    visited[prev_node] = True

    for step in range(1, num_nodes):
        next_node: int = path[step]

        if not g.is_edge(prev_node, next_node):
            return False
        if visited[next_node]:
            return False

        visited[next_node] = True
        prev_node = next_node

    return True


# -------------------------------------------------------
# --- Functions for Eulerian Paths ----------------------
# -------------------------------------------------------


# Works if the graph is fully connected and undirected
def has_eulerian_cycle(g: Graph) -> bool:
    """Checks whether a graph has a valid Eulerian cycle.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    result : bool
        True if the graph contains a Eulerian cycle and False otherwise.
    """
    components: list = dfs_connected_components(g)
    for i in range(g.num_nodes):
        if components[i] != 0:
            return False

        degree: int = g.nodes[i].num_edges()
        if i in g.nodes[i].edges:
            degree += 1
        if degree % 2 == 1:
            return False
    return True


def is_eulerian_cycle(g: Graph, path: list) -> bool:
    """Checks whether a path is a valid Eulerian cycle.

    Parameters
    ----------
    g : Graph
        The input graph.
    path : list of int
        For each node the index of the node preceding it on the path.

    Returns
    -------
    result : bool
        True if the path is a Eulerian cycle and False otherwise.
    """
    num_nodes: int = len(path)
    if num_nodes == 0:
        return g.num_nodes == 0

    used: dict = {}
    for node in g.nodes:
        for edge in node.get_edge_list():
            used[(edge.from_node, edge.to_node)] = False

    prev_node: int = path[0]
    for step in range(1, num_nodes):
        next_node: int = path[step]
        if not g.is_edge(prev_node, next_node):
            return False
        if used[(prev_node, next_node)]:
            return False

        used[(prev_node, next_node)] = True
        if g.undirected:
            used[(next_node, prev_node)] = True

        prev_node = next_node

    for value in used.values():
        if not value:
            return False
    return path[0] == path[-1]


def hierholzers(g: Graph) -> Union[list, None]:
    """Hierholzers algorithm for finding Eulerian cycles.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    full_cycle : list of int
        A list of node indices representing the Eulerian cycle.
    """
    if not has_eulerian_cycle(g):
        return None

    g_r: Graph = g.make_copy()
    options: set = set([0])
    full_cycle: list = [0]

    while len(options) > 0:
        start: int = options.pop()
        current: int = start
        subcycle: list = [start]

        while current != start or len(subcycle) == 1:
            neighbor: int = list(g_r.nodes[current].edges.keys())[0]
            subcycle.append(neighbor)
            g_r.remove_edge(current, neighbor)

            new_num_edges: int = g_r.nodes[current].num_edges()
            if new_num_edges > 0:
                options.add(current)
            elif new_num_edges == 0 and current in options:
                options.remove(current)

            current = neighbor

        if g_r.nodes[start].num_edges() == 0 and start in options:
            options.remove(start)

        loc: int = full_cycle.index(start)
        full_cycle = full_cycle[0:loc] + subcycle + full_cycle[loc + 1 :]

    return full_cycle
