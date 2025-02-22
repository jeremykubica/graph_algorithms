"""Functions for computing cliques in a graph (chapter 17).

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


def is_clique(g: Graph, nodes: list) -> bool:
    """A function to test whether a set of nodes is a valid clique.

    Parameters
    ----------
    g : Graph
        The input graph.
    nodes : list
        The indices of the nodes to test.

    Returns
    -------
    bool
        True if the nodes are a valid clique.
    """
    num_nodes: int = len(nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if not g.is_edge(nodes[i], nodes[j]):
                return False
    return True


def clique_expansion_options(g: Graph, clique: list) -> list:
    """Find all of the nodes that can be added to the current clique
    while having it remain a valid clique.

    Parameters
    ----------
    g : Graph
        The input graph.
    clique : list
        The indices of the current set of nodes.

    Returns
    -------
    options : list
        The indices of the nodes that can be added.
    """
    options: list = []
    for i in range(g.num_nodes):
        if i not in clique:
            valid: bool = True
            for j in clique:
                valid = valid and g.is_edge(i, j)
            if valid:
                options.append(i)
    return options


def clique_greedy(g: Graph) -> list:
    """Construct a clique by greedily adding one node at a time.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    clique : list of int
        The indices of the nodes in the clique.
    """
    clique: list = []
    to_add: list = clique_expansion_options(g, clique)
    while len(to_add) > 0:
        clique.append(to_add[0])
        to_add = clique_expansion_options(g, clique)
    return clique


def maximum_clique_recursive(g: Graph, clique: list, index: int) -> list:
    """The inner function for a recursive backtracking search to find the maximum clique.

    Parameters
    ----------
    g : Graph
        The input graph.
    clique : list
        The indices of the nodes in the current clique.
    index : int
        The index of the current node to test.

    Returns
    -------
    best : list of int
        The indices of the nodes in the best clique found so far.
    """
    if index >= g.num_nodes:
        return copy.copy(clique)

    best: list = maximum_clique_recursive(g, clique, index + 1)

    can_add: bool = True
    for n in clique:
        can_add = can_add and g.is_edge(n, index)

    if can_add:
        clique.append(index)
        candidate: list = maximum_clique_recursive(g, clique, index + 1)
        clique.pop()

        if len(candidate) > len(best):
            best = candidate

    return best


def maximum_clique_backtracking(g: Graph) -> list:
    """The outer wrapper function for a recursive backtracking search to find the maximum clique.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    list of int
        The indices of the nodes in the best clique found.
    """
    return maximum_clique_recursive(g, [], 0)


def maximum_clique_exh(g: Graph) -> list:
    """An exhaustive iterative search for finding the maximum clique (for testing).

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    max_clique : list of int
        The indices of the nodes in the best clique found.
    """
    options: list = [False, True]
    max_clique: list = []

    for counter in itertools.product(options, repeat=g.num_nodes):
        current: list = []
        for i in range(g.num_nodes):
            if counter[i]:
                current.append(i)

        if len(current) > len(max_clique) and is_clique(g, current):
            max_clique = current
    return max_clique
