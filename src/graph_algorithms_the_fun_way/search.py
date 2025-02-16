"""Common graph search algorithms: BFS (Chapter 5), DFS (Chapter 4),
Greedy (Chapter 8), and A* (Chapter 8).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import math
import queue

from graph_algorithms_the_fun_way.graph import Graph, Node
from graph_algorithms_the_fun_way.priorityqueue import PriorityQueue


def breadth_first_search(g: Graph, start: int) -> list:
    """Perform breadth first search from a given starting node.

    Parameters
    ----------
    g : Graph
        The input graph.
    start : int
        The index of the starting node.

    Returns
    -------
    last : list of int
        A list of previous nodes for all nodes in the graph.
    """
    seen: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    pending: queue.Queue = queue.Queue()

    pending.put(start)
    seen[start] = True

    while not pending.empty():
        index: int = pending.get()
        current: Node = g.nodes[index]

        for edge in current.get_edge_list():
            neighbor: int = edge.to_node
            if not seen[neighbor]:
                pending.put(neighbor)
                seen[neighbor] = True
                last[neighbor] = index

    return last


def dfs_recursive_basic(g: Graph, ind: int, seen: list):
    """The recursive function for the basic depth-first search.

    Parameters
    ----------
    g : Graph
        The input graph.
    ind : int
        The index of the current node.
    seen : list of bool
        Whether each node in the graph has been marked seen.
    """
    seen[ind] = True
    current: Node = g.nodes[ind]

    for edge in current.get_edge_list():
        neighbor: int = edge.to_node
        if not seen[neighbor]:
            dfs_recursive_basic(g, neighbor, seen)


def depth_first_search_basic(g: Graph, start: int):
    """The outer wrapper for the basic depth-first search.

    Parameters
    ----------
    g : Graph
        The input graph.
    start : int
        The index of the starting node.
    """
    seen: list = [False] * g.num_nodes
    dfs_recursive_basic(g, start, seen)


def depth_first_search_basic_all(g: Graph):
    """An extension of the basic depth-first search that starts a search from
    each unvisited node.

    Parameters
    ----------
    g : Graph
        The input graph.
    """
    seen: list = [False] * g.num_nodes
    for ind in range(g.num_nodes):
        if not seen[ind]:
            dfs_recursive_basic(g, ind, seen)


def dfs_recursive_path(g: Graph, ind: int, seen: list, last: list):
    """The recursive function for the basic depth-first search
    that also returns the path of previous nodes.

    Parameters
    ----------
    g : Graph
        The input graph.
    ind : int
        The index of the current node.
    seen : list of bool
        Whether each node in the graph has been marked seen.
    last : list of int
        The previous node of each node on the path.
    """
    seen[ind] = True
    current: Node = g.nodes[ind]

    for edge in current.get_edge_list():
        neighbor: int = edge.to_node
        if not seen[neighbor]:
            last[neighbor] = ind
            dfs_recursive_path(g, neighbor, seen, last)


def depth_first_search_path(g: Graph) -> list:
    """The outer wrapper function for the basic depth-first search
    that also returns the path of previous nodes.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    last : list of int
        The previous node of each node on the path.
    """
    seen: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes

    for ind in range(g.num_nodes):
        if not seen[ind]:
            dfs_recursive_path(g, ind, seen, last)
    return last


def depth_first_search_stack(g: Graph, start: int) -> list:
    """A depth-first search using a stack.

    Parameters
    ----------
    g : Graph
        The input graph.
    start : int
        The index of the starting node.

    Returns
    -------
    last : list of int
        The previous node of each node on the path.
    """
    seen: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    to_explore: list = []

    to_explore.append(start)
    while to_explore:
        ind = to_explore.pop()
        if not seen[ind]:
            current: Node = g.nodes[ind]
            seen[ind] = True

            all_edges: list = current.get_sorted_edge_list()
            all_edges.reverse()
            for edge in all_edges:
                neighbor: int = edge.to_node
                if not seen[neighbor]:
                    last[neighbor] = ind
                    to_explore.append(neighbor)

    return last


def dfs_recursive_cc(g: Graph, ind: int, component: list, curr_comp: int):
    """The recursive helper function for the depth-first connected component search.

    Parameters
    ----------
    g : Graph
        The input graph.
    ind : int
        The index of the current node.
    component : list of int
        The nodes in the current connected component.
    curr_comp : int
        The index of the current component.
    """
    component[ind] = curr_comp
    current: Node = g.nodes[ind]

    for edge in current.get_edge_list():
        neighbor: int = edge.to_node
        if component[neighbor] == -1:
            dfs_recursive_cc(g, neighbor, component, curr_comp)


def dfs_connected_components(g: Graph) -> list:
    """Perform a depth-first search to find the connected components.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    component : list of list
        A list of connected components.
    """
    component: list = [-1] * g.num_nodes
    curr_comp: int = 0

    for ind in range(g.num_nodes):
        if component[ind] == -1:
            dfs_recursive_cc(g, ind, component, curr_comp)
            curr_comp += 1

    return component


def greedy_search(g: Graph, h: list, start: int, goal: int) -> list:
    """The greedy heuristic search.

    Parameters
    ----------
    g : Graph
        The input graph.
    h : list of float
        A list of the heuristic values for each node.
    start : int
        The index of the starting node.
    goal : int
        The index of the goal node.

    Returns
    -------
    last : list of int
        The previous node of each node on the path.
    """
    visited: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    pq: PriorityQueue = PriorityQueue(min_heap=True)

    pq.enqueue(start, h[start])
    while not pq.is_empty() and not visited[goal]:
        ind: int = pq.dequeue()
        current: Node = g.nodes[ind]
        visited[ind] = True

        for edge in current.get_edge_list():
            neighbor: int = edge.to_node
            if not visited[neighbor] and not pq.in_queue(neighbor):
                pq.enqueue(neighbor, h[neighbor])
                last[neighbor] = ind

    return last


def astar_search(g: Graph, h: list, start: int, goal: int) -> list:
    """The A* heuristic search.

    Parameters
    ----------
    g : Graph
        The input graph.
    h : list of float
        A list of the heuristic values for each node.
    start : int
        The index of the starting node.
    goal : int
        The index of the goal node.

    Returns
    -------
    last : list of int
        The previous node of each node on the path.
    """
    visited: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    cost: list = [math.inf] * g.num_nodes
    pq: PriorityQueue = PriorityQueue(min_heap=True)

    pq.enqueue(start, h[start])
    cost[start] = 0.0

    while not pq.is_empty() and not visited[goal]:
        ind: int = pq.dequeue()
        current: Node = g.nodes[ind]
        visited[ind] = True

        for edge in current.get_edge_list():
            neighbor: int = edge.to_node
            if cost[neighbor] > cost[ind] + edge.weight:
                cost[neighbor] = cost[ind] + edge.weight
                last[neighbor] = ind

                est_value: float = cost[neighbor] + h[neighbor]
                if pq.in_queue(neighbor):
                    pq.update_priority(neighbor, est_value)
                else:
                    pq.enqueue(neighbor, est_value)

    return last
