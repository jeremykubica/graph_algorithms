"""The core data structures for the adjacency matrix representations of a graph.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""


class GraphMatrix:
    """Adjacency matrix representations of a graph structure.

    Note that a production version of this code should use optimized
    matrix libraries, such as NumPy.

    Attributes
    ----------
    connections : list of list
        The matrix of edge weights.
    num_nodes : int
        The total number of nodes in the graph.
    undirected : bool
        A Boolean indicating whether the graph is undirected (True) or
        directed (False).
    """

    def __init__(self, num_nodes: int, undirected: bool = False):
        self.num_nodes: int = num_nodes
        self.undirected: bool = undirected
        self.connections = [[0.0] * num_nodes for _ in range(num_nodes)]

    def set_edge(self, from_node: int, to_node: int, weight: float):
        """Add, modify, or remove an edge in the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.
        weight : float
            The weight of the edge. If 0.0 this effectively
            removes the edge.
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError

        self.connections[from_node][to_node] = weight
        if self.undirected:
            self.connections[to_node][from_node] = weight

    def get_edge(self, from_node: int, to_node: int) -> float:
        """Lookup an edge in the graph.

        Parameters
        ----------
        from_node : int
            The node index of the edge's origin.
        to_node : int
            The node index to the edge's destination.

        Returns
        -------
        weight : float
            The weight of the edge (0.0 if the edge does not exist).
        """
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        return self.connections[from_node][to_node]

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
            True if the graph contains an edge with non-zero weight from
            from_node to to_node and False otherwise.
        """
        return self.get_edge(from_node, to_node) != 0.0

    def print_matrix(self):
        """Display the graph as an adjacency matrix."""
        for j in range(self.num_nodes):
            s = ""
            for k in range(self.num_nodes):
                s = "%s %5.1f" % (s, self.self.connections[j][k])
            print(s)

    def simulate_random_step(self, Vt: list) -> list:
        """Simulate a random step on a graph.

        Parameters
        ----------
        Vt : list of float
            A list providing the probability that the random walk is
            at each node before the step. Must sum to one.

        Returns
        -------
        Vnext : list of float
            A list providing the probability that the random walk is
            at each node after the step.
        """
        if len(Vt) != self.num_nodes:
            raise ValueError("Incorrect length of probability dist")

        Vnext: list = [0.0] * self.num_nodes
        for j in range(self.num_nodes):
            for i in range(self.num_nodes):
                Vnext[j] += Vt[i] * self.connections[i][j]
        return Vnext
