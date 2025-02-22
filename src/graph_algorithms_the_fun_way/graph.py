"""The core data structures for the adjacency list representations of a graph.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import random
from typing import Union


class Edge:
    """Edge objects are containers to store information about graph edges.

    Attributes
    ----------
    from_node : int
        The node index of the edge's origin.
    to_node : int
        The node index to the edge's destination.
    weight : float
        The weight of the edge.
    """

    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node: int = from_node
        self.to_node: int = to_node
        self.weight: float = weight

    def print_edge(self):
        """Display the edge information in a human readable form."""
        print(f"{self.from_node} -> {self.to_node} = {self.weight}")


class Node:
    """Node objects contain information for the graph's nodes and
    methods that modify or operate on them.

    Attributes
    ----------
    edges : dict
        A dictionary mapping the destination node's index to the
        corresponding Edge object.
    index : int
        The node's unique numerical index.
    label : any
        An additional label for the node.
    """

    def __init__(self, index: int, label=None):
        self.index: int = index
        self.edges: dict = {}
        self.label = label

    def num_edges(self) -> int:
        """Returns the number of edges."""
        return len(self.edges)

    def get_edge(self, neighbor: int) -> Union[Edge, None]:
        """Returns an edge or None if no such edge exists.

        Parameters
        ----------
        neighbor : int
            The index of the destination node.

        Returns
        -------
        edge : Edge or None
            The Edge object linking the current node and the neighbor or
            None if no such edge exists.
        """
        if neighbor in self.edges:
            return self.edges[neighbor]
        return None

    def add_edge(self, neighbor: int, weight: float):
        """Add an edge to the graph.

        Parameters
        ----------
        neighbor : int
            The index of the neighboring node.
        weight : float
            The weight of the edge.
        """
        self.edges[neighbor] = Edge(self.index, neighbor, weight)

    def remove_edge(self, neighbor: int):
        """Remove an edge from the graph.

        Parameters
        ----------
        neighbor : int
            The index of the neighboring node.
        """
        if neighbor in self.edges:
            del self.edges[neighbor]

    def get_edge_list(self) -> list:
        """Return a list of all edges out of this node.

        Returns
        -------
        edges : list
            The edges in from this node.
        """
        return list(self.edges.values())

    def get_sorted_edge_list(self) -> list:
        """Return a list of all edges out of this node
        sorted by neighbor index.

        Returns
        -------
        edges : list
            The edges in from this node.
        """
        result = []
        neighbors = (list)(self.edges.keys())
        neighbors.sort()

        for n in neighbors:
            result.append(self.edges[n])
        return result

    def get_neighbors(self) -> set:
        """Return a set of the indices to all neighbors in the edge dictionary.
        For undirected graphs this includes all neighbors. For directed graphs,
        this only includes out-neighbors.

        Returns
        -------
        neighbors : set
            The indices to all neighbors in the edge dictionary.
        """
        neighbors: set = set()
        for edge in self.edges.values():
            neighbors.add(edge.to_node)
        return neighbors

    def get_out_neighbors(self) -> set:
        """Return a set of the indices to all neighbors in the edge dictionary.
        For undirected graphs this includes all neighbors. For directed graphs,
        this only includes out-neighbors.

        Returns
        -------
        neighbors : set
            The indices to all neighbors in the edge dictionary.
        """
        neighbors: set = set()
        for edge in self.edges.values():
            neighbors.add(edge.to_node)
        return neighbors

    def is_same_structure(self, n2) -> bool:
        """A testing function that returns True if two nodes have the
        same outgoing edges (same neighbors and weights).

        Returns
        -------
        is_same : bool
            True if the edge structure of the nodes is the same and False otherwise.
        """
        if self.index != n2.index:
            return False
        if len(self.edges) != len(n2.edges):
            return False
        for neighbor in self.edges.keys():
            if neighbor not in n2.edges:
                return False

            w1 = self.edges[neighbor].weight
            w2 = n2.edges[neighbor].weight
            if abs(w1 - w2) > 1e-12:
                return False
        return True

    def out_degree(self):
        """Returns the out-degree of the node."""
        return len(self.edges)

    def undirected_degree(self):
        """Return the undirected degree of a node."""
        count: int = len(self.edges)
        if self.index in self.edges:
            count += 1
        return count

    def print_node(self):
        """Print a human readable representation of the node's structure."""
        if self.label is None:
            print("Node %i:" % self.index)
        else:
            print("Node %i (label=%i):" % (self.index, str(self.label)))
        for neighbor in self.edges:
            self.edges[neighbor].print_edge()


class Graph:
    """Adjacency list representations of a graph structure.

    Attributes
    ----------
    nodes : list
        A list of Node objects, one for each node in the graph.
    node_indices : dict
        A dictionary mapping the a string (the node's name) to its index.
    num_nodes : int
        The total number of nodes in the graph.
    undirected : bool
        A Boolean indicating whether the graph is undirected (True) or
        directed (False).
    """

    def __init__(self, num_nodes: int, undirected: bool = False):
        self.num_nodes: int = num_nodes
        self.undirected: bool = undirected
        self.nodes: list = [Node(j) for j in range(num_nodes)]
        self.node_indices: dict = {}

    def insert_node(self, label=None) -> Node:
        """Add a new node to the graph.

        Parameters
        ----------
        label : any, optional
            The node's (optional) label.

        Returns
        -------
        new_node : Node
            The newly created Node object.
        """
        new_node: Node = Node(self.num_nodes, label=label)
        self.nodes.append(new_node)
        self.num_nodes += 1
        return new_node

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        """Add a new edge to the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.
        weight : float
            The weight of the edge.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError

        self.nodes[from_node].add_edge(to_node, weight)
        if self.undirected:
            self.nodes[to_node].add_edge(from_node, weight)

    def remove_edge(self, from_node: int, to_node: int):
        """Remove an existing edge to the graph if it exists.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError

        self.nodes[from_node].remove_edge(to_node)
        if self.undirected:
            self.nodes[to_node].remove_edge(from_node)

    def add_random_edges(self, num_add: int, allow_self_edges: bool = True):
        """Add a set number of edges between randomly selected nodes. Used for testing.

        Parameters
        ----------
        num_add : int
            The number of edges to add.
        allow_self_edges : bool
            Allow edges from a node back to itself.
        """
        for i in range(num_add):
            a: int = int(random.random() * self.num_nodes)
            b: int = int(random.random() * self.num_nodes)
            if not allow_self_edges:
                while a == b:
                    b = int(random.random() * self.num_nodes)
            self.insert_edge(a, b, random.random() * 99.0 + 1.0)

    def get_edge(self, from_node: int, to_node: int) -> Union[Edge, None]:
        """Lookup an edge in the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.

        Returns
        -------
        edge : Edge or None
            The corresponding Edge object if an edge exists or None
            if no such edge exists.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        return self.nodes[from_node].get_edge(to_node)

    def is_edge(self, from_node: int, to_node: int) -> bool:
        """Check if an edge is in the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.

        Returns
        -------
        result : bool
            True if the graph contains an edge from from_node to to_node
            and False otherwise.
        """
        return self.get_edge(from_node, to_node) is not None

    def make_edge_list(self) -> list:
        """Return a list containing all edges in the graph.

        Returns
        -------
        all_edges : list
            A list of Edge objects containing all edges in the graph.
        """
        all_edges: list = []
        for node in self.nodes:
            for edge in node.edges.values():
                all_edges.append(edge)
        return all_edges

    def get_in_neighbors(self, target: int) -> set:
        """Return a list of all node indices such that those nodes
        have edges to the given target node.

        Parameters
        ----------
        target : int
            The index of the destination node.

        Returns
        -------
        neighbors : set
            The set of the in-neighbors' indices for the given node.
        """
        neighbors: set = set()
        for node in self.nodes:
            if target in node.edges:
                neighbors.add(node.index)
        return neighbors

    def get_index_by_name(self, name: str) -> int:
        """Look up a node by its name. If no node with the name exists,
        the function creates a new node with that name.

        Parameters
        ----------
        name : str
            The name of the node.

        Returns
        -------
        index : int
            The index of the node.
        """
        if name not in self.node_indices:
            new_node: Node = self.insert_node()
            self.node_indices[name] = new_node.index
        return self.node_indices[name]

    def make_undirected_neighborhood_subgraph(self, ind: int, closed: bool):
        """Create the subgraph of neighbors to a given node in an undirected graph.

        Parameters
        ----------
        ind : int
            The index of the query node.
        closed : bool
            Indicates whether to include the given node (True) or not (False).

        Returns
        -------
        g_new : Graph
            The subgraph consisting of the node's neighborhood.
        """
        if not self.undirected:
            raise ValueError

        nodes_to_use: set = self.nodes[ind].get_neighbors()
        if closed:
            nodes_to_use.add(ind)

        index_map = {}
        for new_index, old_index in enumerate(nodes_to_use):
            index_map[old_index] = new_index

        g_new: Graph = Graph(len(nodes_to_use), undirected=True)
        for n in nodes_to_use:
            for edge in self.nodes[n].get_edge_list():
                if edge.to_node in nodes_to_use and edge.to_node > n:
                    ind1_new = index_map[n]
                    ind2_new = index_map[edge.to_node]
                    g_new.insert_edge(ind1_new, ind2_new, edge.weight)

        return g_new

    def label_node(self, node: int, label):
        """Adds a label to a node.

        Parameters
        ----------
        node : int
            The index of the node.
        label : any
            The label to attach.
        """
        if node >= 0 and node < self.num_nodes:
            self.nodes[node].label = label

    def is_unlabeled(self) -> bool:
        """Return whether the graph is completely unlabeled."""
        for n in self.nodes:
            if n.label is not None:
                return False
        return True

    def reset_labels(self):
        """Set all of the node's labels to None."""
        for n in self.nodes:
            n.label = None

    def print_adj_list(self):
        """Display the graph in adjacency list format."""
        for j in range(self.num_nodes):
            n = self.nodes[j]
            s = "%2i:" % j
            if n.label is not None:
                s = "%2i (%s):" % (j, str(n.label))
            for edge in n.edges.values():
                s = "%s  %2i (%.2f)" % (s, edge.to_node, edge.weight)
            print(s)

    def is_valid(self, allow_negative_weights=True, verbose=False) -> bool:
        """Determine whether the Graph is valid (all indices are in bounds,
        edges point to valid nodes, etc.). Used for testing only.
        """
        edge_count = 0

        if self.num_nodes != len(self.nodes):
            if verbose:
                print("Graph size mismatch %i vs %i" % (self.num_nodes, len(self.nodes)))
            return False
        for i in range(self.num_nodes):
            node = self.nodes[i]
            if node.index != i:
                if verbose:
                    print("Node id mismatch %i vs %i" % (i, node.index))
                return False
            for edge in node.edges.values():
                edge_count = edge_count + 1
                if edge.from_node != i:
                    if verbose:
                        print("Edge FROM mismatch %i vs %i" % (i, edge.from_node))
                    return False
                if edge.to_node < 0 or edge.to_node >= self.num_nodes:
                    if verbose:
                        print("Edge TO range error %i" % edge.to_node)
                    return False
                if not allow_negative_weights and edge.weight < 0.0:
                    if verbose:
                        print("Edge weight range error %f" % edge.weight)
                    return False
        return True

    def is_same_structure(self, g2) -> bool:
        """Check that two graphs share the same structure: The number of nodes and
        the same connectivity (edges and weights without regard to ordering).
        Labels are not examined. Used for testing.

        Parameters
        ----------
        g2 : Graph
            The graph to compare.

        Returns
        -------
        is_same_structure : bool
            Whether the graphs share the same structure.
        """
        if self.num_nodes != g2.num_nodes:
            return False

        idx = 0
        while idx < self.num_nodes:
            if not self.nodes[idx].is_same_structure(g2.nodes[idx]):
                return False
            idx = idx + 1
        return True

    def make_copy(self):
        """Create and return a copy of the graph."""
        g2: Graph = Graph(self.num_nodes, undirected=self.undirected)
        for node in self.nodes:
            g2.nodes[node.index].label = node.label
            for edge in node.edges.values():
                g2.insert_edge(edge.from_node, edge.to_node, edge.weight)
        return g2


def make_graph_from_edges(num_nodes: int, undirected: bool, edge_list: list) -> Graph:
    """Make a graph from a list of edges (from Appendix A).

    Parameters
    ----------
    num_nodes : int
        The total number of nodes in the graph.
    undirected : bool
        A Boolean indicating whether the graph is undirected (True) or
        directed (False).
    edge_list : list of Edge
        The list of edges to add.

    Returns
    -------
    g : Graph
        The constructed Graph.
    """
    g: Graph = Graph(num_nodes, undirected)
    for edge in edge_list:
        g.insert_edge(edge.from_node, edge.to_node, edge.weight)
    return g


def make_transpose_graph(g: Graph) -> Graph:
    """Create the transpose of a directed graph.

    Parameters
    ----------
    g : Graph
        The graph to transpose.

    Returns
    -------
    g2 : Graph
        The transposed graph.
    """
    g2: Graph = Graph(g.num_nodes, undirected=g.undirected)
    for node in g.nodes:
        for edge in node.get_edge_list():
            g2.insert_edge(edge.to_node, edge.from_node, edge.weight)
    return g2


def edge_in_list(edges: list, u: int, v: int, undirected: bool) -> bool:
    """A testing function that checks if a given edge is in a list of all edges.

    Parameters
    ----------
    edges : list
        A list of Edge objects.
    u : int
        The index of the origin node for the edge.
    v : int
        The index of the destination node for the edge.
    undirected : bool
        Whether the node is undirected (True) or not (False).

    Returns
    -------
    bool
        True if the edge was found in the list and False otherwise.
    """
    for e in edges:
        if v == e.to_node and u == e.from_node:
            return True
        if undirected and u == e.to_node and v == e.from_node:
            return True
    return False
