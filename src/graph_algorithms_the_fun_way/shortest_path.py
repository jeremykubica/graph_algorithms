"""Algorithms for shortest path computations (chapter 7)

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
from graph_algorithms_the_fun_way.priorityqueue import PriorityQueue


def Dijkstras(g: Graph, start_index: int) -> list:
    """Dijkstras for shortest paths.

    Parameters
    ----------
    g : Graph
        The input graph.
    start_index : int
        The index of the starting node.

    Returns
    -------
    last : list of int
        The previous node's index for each node on the path.
    """
    cost: list = [math.inf] * g.num_nodes
    last: list = [-1] * g.num_nodes
    pq: PriorityQueue = PriorityQueue(min_heap=True)

    pq.enqueue(start_index, 0.0)
    for i in range(g.num_nodes):
        if i != start_index:
            pq.enqueue(i, math.inf)
    cost[start_index] = 0.0

    while not pq.is_empty():
        index: int = pq.dequeue()

        for edge in g.nodes[index].get_edge_list():
            neighbor: int = edge.to_node

            if pq.in_queue(neighbor):
                new_cost = cost[index] + edge.weight
                if new_cost < cost[neighbor]:
                    pq.update_priority(neighbor, new_cost)
                    last[neighbor] = index
                    cost[neighbor] = new_cost

    return last


def BellmanFord(g: Graph, start_index: int) -> Union[list, None]:
    """Bellman-Ford algorithm for shortest path.

    Parameters
    ----------
    g : Graph
        The input graph.
    start_index : int
        The index of the starting node.

    Returns
    -------
    last : list of int or None
        The previous node's index for each node on the path. Returns None if
        the graph contains a negative cost cycle.
    """
    cost: list = [math.inf] * g.num_nodes
    last: list = [-1] * g.num_nodes
    all_edges: list = g.make_edge_list()
    cost[start_index] = 0.0

    for itr in range(g.num_nodes - 1):
        for edge in all_edges:
            cost_thr_node: float = cost[edge.from_node] + edge.weight
            if cost_thr_node < cost[edge.to_node]:
                cost[edge.to_node] = cost_thr_node
                last[edge.to_node] = edge.from_node

    for edge in all_edges:
        if cost[edge.to_node] > cost[edge.from_node] + edge.weight:
            return None
    return last


def FloydWarshall(g: Graph) -> list:
    """Floyd-Warshall algorithm for all-pairs shortest path.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    last : list of list of int
        The previous node's index for each node on the path.
    """
    N: int = g.num_nodes
    cost: list = [[math.inf] * N for _ in range(N)]
    last: list = [[-1] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == j:
                cost[i][j] = 0.0
            else:
                edge: Union[Edge, None] = g.get_edge(i, j)
                if edge is not None:
                    cost[i][j] = edge.weight
                    last[i][j] = i

    for k in range(N):
        for i in range(N):
            for j in range(N):
                if cost[i][j] > cost[i][k] + cost[k][j]:
                    cost[i][j] = cost[i][k] + cost[k][j]
                    last[i][j] = last[k][j]

    return last


def GraphDiameter(g: Graph) -> float:
    """Compute the graph's diameter.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    max_cost : float
        The graph's diameter.
    """
    last: list = FloydWarshall(g)
    max_cost: float = -math.inf

    for i in range(g.num_nodes):
        for j in range(g.num_nodes):
            cost: float = 0.0
            current: int = j

            while current != i:
                prev: int = last[i][current]
                if prev == -1:
                    return math.inf

                edge: Union[Edge, None] = g.get_edge(prev, current)
                cost = cost + edge.weight
                current = prev

            if cost > max_cost:
                max_cost = cost

    return max_cost
