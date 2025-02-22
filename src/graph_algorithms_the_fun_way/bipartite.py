"""Algorithms for bipartite matching (Chapter 15).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import copy
import queue
from typing import Union

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.maxflow import edmonds_karp, ResidualGraph


def bipartite_labeling(g: Graph) -> Union[list, None]:
    """Label the nodes according to their side in a bipartite graph.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    label : list or None
        If there is a valid labeling, returns a list of each node's label.
        Otherwise returns None.
    """
    label: list = [None] * g.num_nodes
    pending: queue.Queue = queue.Queue()

    for start in range(g.num_nodes):
        if label[start] is not None:
            continue

        pending.put(start)
        label[start] = True
        while not pending.empty():
            current: int = pending.get()
            next_label = not label[current]

            for edge in g.nodes[current].get_edge_list():
                neighbor: int = edge.to_node
                if label[neighbor] is None:
                    pending.put(neighbor)
                    label[neighbor] = next_label
                elif label[neighbor] != next_label:
                    return None
    return label


class Matching:
    """A data structure for collecting matching information.

    Attributes
    ----------
    num_nodes : int
        The number of nodes in the graph.
    assignments : list
        Maps each node's index to the index of the matched node
        with -1 for no match.
    score : float
        The score of this match.
    """

    def __init__(self, num_nodes: int):
        self.num_nodes: int = num_nodes
        self.assignments: list = [-1] * num_nodes
        self.score: float = 0.0

    def add_edge(self, ind1: int, ind2: int, score: float):
        """Add an edge to the matching.

        Parameters
        ----------
        ind1 : int
            The index of one of the edge's end points.
        ind2 : int
            The index of the other end point.
        score : float
            The score of the edge.
        """
        if ind1 < 0 or ind1 >= self.num_nodes or self.assignments[ind1] != -1:
            raise ValueError(f"Invalid assignment of {ind1}")
        if ind2 < 0 or ind2 >= self.num_nodes or self.assignments[ind2] != -1:
            raise ValueError(f"Invalid assignment of {ind2}")
        self.assignments[ind1] = ind2
        self.assignments[ind2] = ind1
        self.score += score

    def remove_edge(self, ind1: int, ind2: int, score: float):
        """Remove an edge from the matching.

        Parameters
        ----------
        ind1 : int
            The index of one of the edge's end points.
        ind2 : int
            The index of the other end point.
        score : float
            The score of the edge.
        """
        if ind1 < 0 or ind1 >= self.num_nodes:
            raise ValueError(f"Invalid assignment of {ind1}")
        if ind2 < 0 or ind2 >= self.num_nodes:
            raise ValueError(f"Invalid assignment of {ind2}")
        self.assignments[ind1] = -1
        self.assignments[ind2] = -1
        self.score -= score


def bipartite_matching_exh(g: Graph) -> Union[list, None]:
    """The exhaustive algorithm to find a maximum-weight matching.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    list or None
        Maps each node's index to the index of the matched node
        with -1 for no match. Returns None if the graph is not bipartite.
    """
    labels: Union[list, None] = bipartite_labeling(g)
    if labels is None:
        return None

    current: Matching = Matching(g.num_nodes)
    best_matching: Matching = matching_recursive(g, labels, current, 0)
    return best_matching.assignments


def matching_recursive(g: Graph, labels: list, current: Matching, index: int) -> Matching:
    """The recursive implementation of the exhaustive algorithm to find a maximum-weight matching.

    Parameters
    ----------
    g : Graph
        The input graph.
    labels : list
        A list of each node's label.
    current : Matching
        The information about the current matching.
    index : int
        The current node's index.

    Returns
    -------
    best : Matching
        The information about the best matching found so far.
    """
    if index >= g.num_nodes:
        return copy.deepcopy(current)
    if not labels[index]:
        return matching_recursive(g, labels, current, index + 1)

    best: Matching = matching_recursive(g, labels, current, index + 1)
    for edge in g.nodes[index].get_edge_list():
        if current.assignments[edge.to_node] == -1:
            current.add_edge(index, edge.to_node, edge.weight)
            new_m: Matching = matching_recursive(g, labels, current, index + 1)
            if new_m.score > best.score:
                best = new_m
            current.remove_edge(index, edge.to_node, edge.weight)
    return best


def bipartite_matching_max_flow(g: Graph) -> Union[list, None]:
    """The maximum-flow algorithm for maximum-cardinality matching.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    result : list or None
        Maps each node's index to the index of the matched node
        with -1 for no match. Returns None if the graph is not bipartite.
    """
    num_nodes: int = g.num_nodes

    labeling: Union[list, None] = bipartite_labeling(g)
    if labeling is None:
        return None

    extended: Graph = Graph(g.num_nodes + 2, undirected=False)
    for node in g.nodes:
        for edge in node.edges.values():
            if labeling[edge.from_node]:
                extended.insert_edge(edge.from_node, edge.to_node, 1.0)

    source_ind: int = num_nodes
    sink_ind: int = num_nodes + 1
    for i in range(num_nodes):
        if labeling[i]:
            extended.insert_edge(source_ind, i, 1.0)
        else:
            extended.insert_edge(i, sink_ind, 1.0)

    residual: ResidualGraph = edmonds_karp(extended, source_ind, sink_ind)

    result: list = [-1] * g.num_nodes
    for from_node in range(residual.num_nodes):
        if from_node != source_ind:
            edge_list: dict = residual.edges[from_node]
            for to_node in edge_list.keys():
                if to_node != sink_ind and edge_list[to_node].used > 0.0:
                    result[from_node] = to_node
                    result[to_node] = from_node
    return result
