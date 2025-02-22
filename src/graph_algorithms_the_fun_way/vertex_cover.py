"""Functions for computing vertex covers in a graph (chapter 17).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import copy
import itertools

from graph_algorithms_the_fun_way.graph import Graph


def is_vertex_cover(g: Graph, nodes: list) -> bool:
    """A function to test whether a set of nodes is a valid vertex cover.

    Parameters
    ----------
    g : Graph
        The input graph.
    nodes : list
        The nodes to test.

    Returns
    -------
    bool
        True if the nodes are a valid vertex cover.
    """
    node_set: set = set(nodes)
    for edge in g.make_edge_list():
        if edge.from_node not in node_set and edge.to_node not in node_set:
            return False
    return True


def vertex_cover_greedy_choice(g: Graph, nodes: list) -> int:
    """Find the best node to add to the vertex cover based on
    a heuristic of how many new edges are covered.

    Parameters
    ----------
    g : Graph
        The input graph.
    nodes : list
        The current set of nodes.

    Returns
    -------
    best_option : int
        The best node to add according to the heuristic.
    """
    edges_covered: set = set([])
    for index in nodes:
        for edge in g.nodes[index].get_edge_list():
            edges_covered.add((edge.from_node, edge.to_node))
            edges_covered.add((edge.to_node, edge.from_node))

    best_option: int = -1
    best_num_edges: int = 0
    for i in range(g.num_nodes):
        new_covered: int = 0
        for edge in g.nodes[i].get_edge_list():
            if (edge.from_node, edge.to_node) not in edges_covered:
                new_covered = new_covered + 1

        if new_covered > best_num_edges:
            best_num_edges = new_covered
            best_option = i

    return best_option


def vertex_cover_greedy(g: Graph) -> list:
    """Construct a vertex cover set by greedily adding one node at a time.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    nodes : list
        The nodes in the found vertex cover.
    """
    nodes: list = []
    to_add: int = vertex_cover_greedy_choice(g, nodes)
    while to_add != -1:
        nodes.append(to_add)
        to_add = vertex_cover_greedy_choice(g, nodes)
    return nodes


def minimum_vertex_cover_rec(g: Graph, current: set, index: int) -> set:
    """The inner function for a recursive backtracking search to find the minimum vertex cover.

    Parameters
    ----------
    g : Graph
        The input graph.
    current : set
        The nodes in the current set.
    index : int
        The index of the current node to test.

    Returns
    -------
    best : list
        The nodes in the best vertex cover found so far.
    """
    if index >= g.num_nodes:
        return copy.copy(current)

    best: set = minimum_vertex_cover_rec(g, current, index + 1)

    can_remove: bool = True
    for edge in g.nodes[index].get_edge_list():
        can_remove = can_remove and edge.to_node in current

    if can_remove:
        current.remove(index)
        candidate: set = minimum_vertex_cover_rec(g, current, index + 1)
        current.add(index)

        if len(candidate) < len(best):
            best = candidate

    return best


def minimum_vertex_cover_backtracking(g: Graph) -> list:
    """The outer wrapper function for a recursive backtracking search to find the minimum vertex cover.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    list
        The nodes in the best vertex cover found.
    """
    current: set = set([i for i in range(g.num_nodes)])
    best: set = minimum_vertex_cover_rec(g, current, 0)
    return list(best)


def minimum_vertex_cover_exh(g: Graph) -> list:
    """An exhaustive iterative search for finding the minimum vertex cover (for testing).

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    min_cover : list
        The nodes in the best vertex cover found.
    """
    options: list = [False, True]
    min_cover: list = [i for i in range(g.num_nodes)]

    for counter in itertools.product(options, repeat=g.num_nodes):
        current: list = []
        for i in range(g.num_nodes):
            if counter[i]:
                current.append(i)

        if len(current) < len(min_cover) and is_vertex_cover(g, current):
            min_cover = current
    return min_cover
