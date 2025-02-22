"""Functions for computing independent sets in a graph (chapter 17).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import copy
import itertools
import random

from graph_algorithms_the_fun_way.graph import Graph


def is_independent_set(g: Graph, nodes: list) -> bool:
    """A function to test whether a set of nodes is a valid independent set.

    Parameters
    ----------
    g : Graph
        The input graph.
    nodes : list
        The indices of the nodes to test.

    Returns
    -------
    bool
        True if the nodes are a valid independent set.
    """
    num_nodes: int = len(nodes)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if g.is_edge(nodes[i], nodes[j]):
                return False
    return True


def independent_set_expansion_options(g: Graph, current: list) -> list:
    """Find all of the nodes that can be added to the current set
    while having it remain a valid independent set.

    Parameters
    ----------
    g : Graph
        The input graph.
    current : list
        The indices of the nodes to test.

    Returns
    -------
    options : list
        The indices of the nodes that can be added.
    """
    options: list = []
    for i in range(g.num_nodes):
        if i not in current:
            valid: bool = True
            for j in current:
                valid = valid and not g.is_edge(i, j)
            if valid:
                options.append(i)
    return options


def independent_set_lowest_expansion(g: Graph, current: list) -> int:
    """Find the node with the fewest edges that can be added to the
    current set and have it remain a valid independent set.

    Parameters
    ----------
    g : Graph
        The input graph.
    current : list
        The indices of the current set of nodes.

    Returns
    -------
    best_option : int
        The index of the best node to add according to the heuristic.
    """
    best_option: int = -1
    best_num_edges: int = g.num_nodes + 1

    for i in range(g.num_nodes):
        if i not in current and g.nodes[i].num_edges() < best_num_edges:
            valid: bool = True
            for j in current:
                valid = valid and not g.is_edge(i, j)
            if valid:
                best_num_edges = g.nodes[i].num_edges()
                best_option = i
    return best_option


def independent_set_greedy(g: Graph) -> list:
    """Construct an independent set by greedily adding one node at a time.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    i_set : list
        The indices of the nodes in the found independent set.
    """
    i_set: list = []
    to_add: int = independent_set_lowest_expansion(g, i_set)
    while to_add != -1:
        i_set.append(to_add)
        to_add = independent_set_lowest_expansion(g, i_set)
    return i_set


def independent_set_random(g: Graph) -> list:
    """Construct an independent set by randomly adding one node at a time.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    i_set : list of int
        The indices of the nodes in the independent set found.
    """
    i_set: list = []
    options: list = independent_set_expansion_options(g, i_set)
    while len(options) > 0:
        index: int = random.randint(0, len(options) - 1)
        i_set.append(options[index])
        options = independent_set_expansion_options(g, i_set)
    return i_set


def build_independent_set_random(g: Graph, iterations: int) -> list:
    """Construct a better independent set by running multiple random searches.

    Parameters
    ----------
    g : Graph
        The input graph.
    iterations : int
        The number of searches to run.

    Returns
    -------
    best_iset : list of int
        The indices of the nodes in the best independent set found.
    """
    best_iset: list = []
    for i in range(iterations):
        current_iset = independent_set_random(g)
        if len(current_iset) > len(best_iset):
            best_iset = current_iset
    return best_iset


def maximum_independent_set_rec(g: Graph, current: list, index: int) -> list:
    """The inner function for a recursive backtracking search to find the maximum independent set.

    Parameters
    ----------
    g : Graph
        The input graph.
    current : list
        The indices of the nodes in the current independent set.
    index : int
        The index of the current node to test.

    Returns
    -------
    best : list of int
        The indices of the nodes in the best independent set found.
    """
    if index >= g.num_nodes:
        return copy.copy(current)

    best: list = maximum_independent_set_rec(g, current, index + 1)

    can_add: bool = True
    for n in current:
        can_add = can_add and not g.is_edge(n, index)

    if can_add:
        current.append(index)
        candidate: list = maximum_independent_set_rec(g, current, index + 1)
        current.pop()

        if len(candidate) > len(best):
            best = candidate

    return best


def maximum_independent_set_backtracking(g: Graph) -> list:
    """The outer wrapper function for a recursive backtracking search to find the maximum independent set.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    list of int
        The indices of the nodes in the best independent set found.
    """
    return maximum_independent_set_rec(g, [], 0)


def maximum_independent_set_exh(g: Graph) -> list:
    """An exhaustive iterative search for finding the maximum independent set (for testing).

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    max_set : list
        The indices of the nodes in the best independent set found.
    """
    options: list = [False, True]
    max_set: list = []

    for counter in itertools.product(options, repeat=g.num_nodes):
        current: list = []
        for i in range(g.num_nodes):
            if counter[i]:
                current.append(i)

        if len(current) > len(max_set) and is_independent_set(g, current):
            max_set = current
    return max_set
