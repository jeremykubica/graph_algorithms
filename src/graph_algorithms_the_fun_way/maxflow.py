"""Algorithms for finding maximum flow (Chapter 14).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from graph_algorithms_the_fun_way.graph import Graph, Node

import math
import queue
from typing import Union


class CapacityEdge:
    """An object to represent information about edges with capacity.

    Attributes
    ----------
    from_node : int
        The node index of the edge's origin.
    to_node : int
        The node index to the edge's destination.
    capacity : float
        The capacity of the edge.
    used : float
        The amount of capacity used.
    """

    def __init__(self, from_node: int, to_node: int, capacity: float):
        self.from_node: int = from_node
        self.to_node: int = to_node
        self.capacity: float = capacity
        self.used: float = 0.0

    def adjust_used(self, amount: float):
        """Adjust the amount of flow through the edge.

        Parameters
        ----------
        amount : float
            The change in flow.
        """
        if self.used + amount < 0.0 or self.used + amount > self.capacity:
            raise Exception("Capacity Error")
        self.used += amount

    def capacity_left(self) -> float:
        """Compute the capacity remaining."""
        return self.capacity - self.used

    def flow_used(self) -> float:
        """Compute the flow used."""
        return self.used

    def print_edge(self):
        """Print the edge information."""
        print(f"{self.from_node} -> {self.to_node}: Using {self.used} of {self.capacity}")


class ResidualGraph:
    """Adjacency list representations of a graph structure for max flow problems.

    Attributes
    ----------
    num_nodes : int
        The total number of nodes in the graph.
    source_index : int
        The node index of the source node.
    sink_index : int
        The node index of the sink node.
    edges : list of dict
        A list of dictionaries where each node has a dictionary mapping
        that destination index to a CapacityEdge.
    all_neighbors : list of set
        A list of sets where each node has a set of all its neighbors' indices.
    """

    def __init__(self, num_nodes: int, source_index: int, sink_index: int):
        self.num_nodes: int = num_nodes
        self.source_index: int = source_index
        self.sink_index: int = sink_index
        self.edges: list = [{} for _ in range(num_nodes)]
        self.all_neighbors: list = [set() for _ in range(num_nodes)]

    def get_edge(self, from_node: int, to_node: int) -> Union[CapacityEdge, None]:
        """Lookup an edge in the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.

        Returns
        -------
        edge : CapacityEdge or None
            The corresponding CapacityEdge object if an edge exists or None
            if no such edge exists.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        if to_node in self.edges[from_node]:
            return self.edges[from_node][to_node]
        return None

    def insert_edge(self, from_node: int, to_node: int, capacity: float):
        """Add a new edge to the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.
        capacity : float
            The capacity of the edge.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError

        if from_node == self.sink_index:
            raise ValueError("Tried to insert edge FROM sink node.")
        if to_node == self.source_index:
            raise ValueError("Tried to insert edge TO source node.")
        if from_node in self.edges[to_node]:
            raise ValueError(
                f"Tried to insert edge {from_node}->{to_node}, "
                f"edge {to_node}->{from_node} already exists."
            )
        if capacity <= 0:
            raise ValueError(f"Tried to insert capacity {capacity}")

        self.edges[from_node][to_node] = CapacityEdge(from_node, to_node, capacity)
        self.all_neighbors[from_node].add(to_node)
        self.all_neighbors[to_node].add(from_node)

    def compute_total_flow(self) -> float:
        """Compute the total flow through the graph.

        Returns
        -------
        total_flow : float
            The total flow through the graph.
        """
        total_flow: float = 0.0
        for to_node in self.edges[self.source_index]:
            total_flow += self.edges[self.source_index][to_node].flow_used()
        return total_flow

    def get_residual(self, from_node: int, to_node: int) -> float:
        """Compute the residual along an edge.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.

        Return
        ------
        residual : float
            The residual of the edge.
        """
        if to_node not in self.all_neighbors[from_node]:
            return 0

        if to_node in self.edges[from_node]:
            return self.edges[from_node][to_node].capacity_left()
        else:
            return self.edges[to_node][from_node].flow_used()

    def min_residual_on_path(self, last: list) -> float:
        """Compute the minimum residual along a path of nodes.

        Parameters
        ----------
        last : list
            The previous node's index for each node on the path.

        Returns
        -------
        min_val : float
            The minimum residual along a path of nodes.
        """
        min_val: float = math.inf

        current: int = self.sink_index
        while current != self.source_index:
            prev: int = last[current]
            if prev == -1:
                raise ValueError
            min_val = min(min_val, self.get_residual(prev, current))
            current = prev
        return min_val

    def update_along_path(self, last: list, amount: float):
        """Update the flow along each edge in the path.

        Parameters
        ----------
        last : list
            The previous node's index for each node on the path.
        amount : float
            The change in flow along the path.
        """
        current: int = self.sink_index
        while current != self.source_index:
            prev: int = last[current]
            if prev == -1:
                raise ValueError

            if current in self.edges[prev]:
                self.edges[prev][current].adjust_used(amount)
            else:
                self.edges[current][prev].adjust_used(-amount)
            current = prev

    def print_graph(self):
        """Print a user readable representation of the graph."""
        for i in range(self.num_nodes):
            for e in self.edges[i].values():
                e.print_edge()


def augmenting_path_dfs_recursive(g: ResidualGraph, current: int, seen: list, last: list):
    """The recursive inner function to find an augmenting path using depth-first search.

    Parameters
    ----------
    g : ResidualGraph
        The input graph.
    current : int
        The index of the current node.
    seen : list of bool
        Whether each node in the graph has been marked seen.
    last : list of int
        The previous node's index for each node on the path.
    """
    seen[current] = True

    for n in g.all_neighbors[current]:
        if not seen[n] and g.get_residual(current, n) > 0:
            last[n] = current
            if last[g.sink_index] != -1:
                return
            augmenting_path_dfs_recursive(g, n, seen, last)


def find_augmenting_path_dfs(g: ResidualGraph) -> list:
    """The outer wrapper function to find an augmenting path using depth-first search.

    Parameters
    ----------
    g : ResidualGraph
        The input graph.

    Returns
    -------
    last : list of int
        The previous node's index for each node on the path.
    """
    seen: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    augmenting_path_dfs_recursive(g, g.source_index, seen, last)
    return last


def find_augmenting_path_bfs(g: ResidualGraph) -> list:
    """The function to find an augmenting path using breadth-first search.

    Parameters
    ----------
    g : ResidualGraph
        The input graph.

    Returns
    -------
    last : list of int
        The previous node's index for each node on the path.
    """
    seen: list = [False] * g.num_nodes
    last: list = [-1] * g.num_nodes
    pending: queue.Queue = queue.Queue()

    seen[g.source_index] = True
    pending.put(g.source_index)
    while not pending.empty() and not seen[g.sink_index]:
        current: int = pending.get()
        for n in g.all_neighbors[current]:
            if not seen[n] and g.get_residual(current, n) > 0:
                pending.put(n)
                seen[n] = True
                last[n] = current

    return last


def augment_multisource_graph(g: Graph, sources: list) -> int:
    """A function that transforms a multi-source graph into a graph with a single source.

    Parameters
    ----------
    g : ResidualGraph
        The input graph.
    sources : list
        A list of noide indices for each source in the graph.

    Returns
    -------
    new_source : int
        The index of the new source node.
    """
    new_source: Node = g.insert_node()

    total_edge_weight: float = 0
    for node in g.nodes:
        for edge in node.edges.values():
            total_edge_weight += edge.weight

    for old_source in sources:
        g.insert_edge(new_source.index, old_source, total_edge_weight + 1)
    return new_source.index


def augment_multisink_graph(g: Graph, sinks: list) -> int:
    """A function that transforms a multi-sink graph into a graph with a single sink.

    Parameters
    ----------
    g : ResidualGraph
        The input graph.
    sinks : list
        A list of noide indices for each sink in the graph.

    Returns
    -------
    new_sink : int
        The index of the new sink node.
    """
    new_sink: Node = g.insert_node()

    total_edge_weight: float = 0
    for node in g.nodes:
        for edge in node.edges.values():
            total_edge_weight += edge.weight

    for old_sink in sinks:
        g.insert_edge(old_sink, new_sink.index, total_edge_weight + 1)
    return new_sink.index


def ford_fulkerson(g: Graph, source: int, sink: int) -> ResidualGraph:
    """The Ford-Fulkerson algorithm for maximum flow using DFS.

    Parameters
    ----------
    g : Graph
        The input graph.
    source : int
        The index of the source node.
    sink : int
        The index of the sink node.

    Returns
    -------
    residual : ResidualGraph
        A ResidualGraph object with the maximum flow set along its edges.
    """
    residual: ResidualGraph = ResidualGraph(g.num_nodes, source, sink)
    for node in g.nodes:
        for edge in node.edges.values():
            residual.insert_edge(edge.from_node, edge.to_node, edge.weight)

    done = False
    while not done:
        last: list = find_augmenting_path_dfs(residual)
        if last[sink] > -1:
            min_value: float = residual.min_residual_on_path(last)
            residual.update_along_path(last, min_value)
        else:
            done = True

    return residual


def edmonds_karp(g: Graph, source: int, sink: int) -> ResidualGraph:
    """The Edmonds-Karp algorithm for maximum flow.

    Parameters
    ----------
    g : Graph
        The input graph.
    source : int
        The index of the source node.
    sink : int
        The index of the sink node.

    Returns
    -------
    residual : ResidualGraph
        A ResidualGraph object with the maximum flow set along its edges.
    """
    residual: ResidualGraph = ResidualGraph(g.num_nodes, source, sink)
    for node in g.nodes:
        for edge in node.edges.values():
            residual.insert_edge(edge.from_node, edge.to_node, edge.weight)

    done = False
    while not done:
        last: list = find_augmenting_path_bfs(residual)
        if last[sink] > -1:
            min_value: float = residual.min_residual_on_path(last)
            residual.update_along_path(last, min_value)
        else:
            done = True
    return residual
