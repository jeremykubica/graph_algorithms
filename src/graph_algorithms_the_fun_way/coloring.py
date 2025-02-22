"""Functions for graph coloring (chapter 16)

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import itertools

from graph_algorithms_the_fun_way.graph import Graph, Node


def is_graph_coloring_valid(g: Graph) -> bool:
    """Check if a graph coloring is valid.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    bool
        True if the coloring is valid and False otherwise.
    """
    for node in g.nodes:
        if node.label is None:
            return False
        for edge in node.get_edge_list():
            neighbor: Node = g.nodes[edge.to_node]
            if neighbor.label == node.label:
                return False
    return True


def graph_color_brute_force(g: Graph, num_colors: int) -> bool:
    """Perform a brute-force iterative search for a graph coloring.

    Parameters
    ----------
    g : Graph
        The input graph. The nodes' labels are modified in-place to capture the result.
    num_colors : int
        The maximum number of colors to use.

    Returns
    -------
    bool
        True if a valid coloring was found and False otherwise.
    """
    options: list = [i for i in range(1, num_colors + 1)]

    for counter in itertools.product(options, repeat=g.num_nodes):
        for n in range(g.num_nodes):
            g.nodes[n].label = counter[n]
        if is_graph_coloring_valid(g):
            return True

    for n in range(g.num_nodes):
        g.nodes[n].label = None
    return False


def first_unused_color(g: Graph, node_index: int) -> int:
    """Find the lowest color number that is not used by any of the neighbors
    of a given node.

    Parameters
    ----------
    g : Graph
        The input graph.
    node_index : int
        The index of the query node.

    Returns
    -------
    int
        The lowest color number that is not used by any of the neighbors
    """
    used_colors: set = set()
    for edge in g.nodes[node_index].get_edge_list():
        neighbor: Node = g.nodes[edge.to_node]
        if neighbor.label is not None:
            used_colors.add(neighbor.label)

    color: int = 1
    while color in used_colors:
        color = color + 1
    return color


def graph_color_greedy(g: Graph) -> bool:
    """Perform a greedy search for a graph coloring.

    Parameters
    ----------
    g : Graph
        The input graph. The nodes' labels are modified in-place to capture the result.

    Returns
    -------
    bool
        Always returns True since we are not enforcing a maximum number of colors.
    """
    for idx in range(g.num_nodes):
        g.nodes[idx].label = first_unused_color(g, idx)
    return True


def graph_color_dfs(g: Graph, num_colors: int, index: int = 0) -> bool:
    """Perform an exhaustive DFS for a graph coloring.

    Parameters
    ----------
    g : Graph
        The input graph. The nodes' labels are modified in-place to capture the result.
    num_colors : int
        The maximum number of colors to use.
    index : int
        The index of the current node.

    Returns
    -------
    bool
        True if a valid coloring was found and False otherwise.
    """
    if index == g.num_nodes:
        return is_graph_coloring_valid(g)

    for color in range(1, num_colors + 1):
        g.nodes[index].label = color
        if graph_color_dfs(g, num_colors, index + 1):
            return True

    g.nodes[index].label = None
    return False


def graph_color_dfs_pruning(g: Graph, num_colors: int, index: int = 0) -> bool:
    """A DFS with pruning to find a graph coloring.

    Parameters
    ----------
    g : Graph
        The input graph. The nodes' labels are modified in-place to capture the result.
    num_colors : int
        The maximum number of colors to use.
    index : int
        The index of the current node.

    Returns
    -------
    bool
        True if a valid coloring was found and False otherwise.
    """
    if index == g.num_nodes:
        return True

    for color in range(1, num_colors + 1):
        is_usable: bool = True
        for edge in g.nodes[index].get_edge_list():
            if g.nodes[edge.to_node].label == color:
                is_usable = False

        if is_usable:
            g.nodes[index].label = color
            if graph_color_dfs_pruning(g, num_colors, index + 1):
                return True
            g.nodes[index].label = None

    return False


def graph_color_removal(g: Graph, num_colors: int) -> bool:
    """The node removal algorithm described in 'Register Allocation via Coloring'
    by Chaitin et. al. (1981).

    Parameters
    ----------
    g : Graph
        The input graph. The nodes' labels are modified in-place to capture the result.
    num_colors : int
        The maximum number of colors to use.

    Returns
    -------
    bool
        True if a valid coloring was found and False otherwise.
    """
    removed: list = [False] * g.num_nodes
    node_stack: list = []
    g2 = g.make_copy()

    removed_one: bool = True
    while removed_one:
        removed_one = False
        for node in g2.nodes:
            if not removed[node.index] and node.num_edges() < num_colors:
                node_stack.append(node.index)

                all_edges: list = node.get_sorted_edge_list()
                for edge in all_edges:
                    g2.remove_edge(edge.from_node, edge.to_node)

                removed[node.index] = True
                removed_one = True

    if len(node_stack) < g.num_nodes:
        return False

    while len(node_stack) > 0:
        current: int = node_stack.pop()
        g.nodes[current].label = first_unused_color(g, current)

    return True
