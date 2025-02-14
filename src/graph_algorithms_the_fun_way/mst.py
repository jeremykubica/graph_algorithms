"""Algorithms for finding and testing minimum spanning trees.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from typing import Union

from graph_algorithms_the_fun_way.union_find import UnionFind
from graph_algorithms_the_fun_way.graph import Graph, Node
from graph_algorithms_the_fun_way.priorityqueue import PriorityQueue


def is_spanning_tree(g: Graph, edges: Union[list, None]) -> bool:
    """Check whether a list of edges forms a spanning tree of a graph.

    Parameters
    ----------
    g : Graph
        The input graph.
    edges : list, optional
        The list of edges to check as the spanning tree.

    Returns
    -------
    result : bool
        True if the list of edges comprises a spanning tree and False otherwise.
    """
    if edges is None:
        return False

    disjoint_count: int = g.num_nodes
    djs: UnionFind = UnionFind(g.num_nodes)

    for edge in edges:
        if not djs.are_disjoint(edge.to_node, edge.from_node):
            return False
        djs.union_sets(edge.to_node, edge.from_node)
        disjoint_count = disjoint_count - 1

    return disjoint_count == 1


def compute_sum_weights(edges) -> float:
    """Compute the sum of weights for a list of edges.

    Parameters
    ----------
    edges : list
        The list of edges.

    Returns
    -------
    sum_weights : float
        The sum of edge weights.
    """
    sum_weights: float = 0.0
    for edge in edges:
        sum_weights = sum_weights + edge.weight
    return sum_weights


def prims(g: Graph) -> Union[list, None]:
    """Prim's algorithm for finding the minimum spanning tree of a graph.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    mst_edges : list or None
        The list of edges in the minimum spanning tree or None if no
        such tree exists.
    """
    pq: PriorityQueue = PriorityQueue(min_heap=True)
    last: list = [-1] * g.num_nodes
    mst_edges: list = []

    pq.enqueue(0, 0.0)
    for i in range(1, g.num_nodes):
        pq.enqueue(i, float("inf"))

    while not pq.is_empty():
        index: int = pq.dequeue()
        current: Node = g.nodes[index]

        if last[index] != -1:
            mst_edges.append(current.get_edge(last[index]))
        elif index != 0:
            return None

        for edge in current.get_edge_list():
            neighbor: int = edge.to_node
            if pq.in_queue(neighbor):

                if edge.weight < pq.get_priority(neighbor):
                    pq.update_priority(neighbor, edge.weight)
                    last[neighbor] = index

    return mst_edges


def kruskals(g: Graph) -> Union[list, None]:
    """Kruskal's algorithm for finding the minimum spanning tree of a graph.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    mst_edges : list or None
        The list of edges in the minimum spanning tree or None if no
        such tree exists.
    """
    djs: UnionFind = UnionFind(g.num_nodes)
    all_edges: list = []
    mst_edges: list = []

    for idx in range(g.num_nodes):
        for edge in g.nodes[idx].get_edge_list():
            if edge.to_node > edge.from_node:
                all_edges.append(edge)
    all_edges.sort(key=lambda edge: edge.weight)

    for edge in all_edges:
        if djs.are_disjoint(edge.to_node, edge.from_node):
            mst_edges.append(edge)
            djs.union_sets(edge.to_node, edge.from_node)

    if djs.num_disjoint_sets == 1:
        return mst_edges
    else:
        return None
