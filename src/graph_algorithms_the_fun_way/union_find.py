"""An implementation of a basic UnionFind data structure.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""


class UnionFindNode:
    """A node for storing UnionFind information.

    Attributes
    ----------
    label : int
        The label of the node.
    parent : UnionFindNode or None
        A pointer to this node's parent.
    """

    def __init__(self, label: int):
        self.label = label
        self.parent = None


class UnionFind:
    """The UnionFind data structure.

    Attributes
    ----------
    nodes : list of UnionFindNodes
        A list of all the elements (UnionFindNodes) in the disjoint set.
    set_sizes : list of int
        A list of the size of each set.
    num_disjoint_sets : int
        The number of disjoint sets.

    Parameters
    ----------
    num_sets : int
        The initial number of disjoint sets.
    """

    def __init__(self, num_sets: int):
        self.nodes: list = [UnionFindNode(i) for i in range(num_sets)]
        self.set_sizes: list = [1 for i in range(num_sets)]
        self.num_disjoint_sets: int = num_sets

    def find_set(self, label: int) -> int:
        """Find the set ID to which the given element belongs.

        Parameters
        ----------
        label : int
            The label of the element to lookup.

        Returns
        -------
        int
            The ID of the set to which the given element belongs.
        """
        if label < 0 or label >= len(self.nodes):
            raise IndexError

        current: UnionFindNode = self.nodes[label]
        while current.parent is not None:
            current = current.parent
        return current.label

    def are_disjoint(self, label1: int, label2: int) -> bool:
        """Checks whether two elements are in different sets.

        Parameters
        ----------
        label1 : int
            The label of the first element.
        label2 : int
            The label of the second element.

        Returns
        -------
        bool
            True if the elements are in different sets and False otherwise.
        """
        return self.find_set(label1) != self.find_set(label2)

    def union_sets(self, label1: int, label2: int):
        """Union two disjoint sets into a single set.

        Parameters
        ----------
        label1 : int
            The label of the first element.
        label2 : int
            The label of the second element.
        """
        set1_label: int = self.find_set(label1)
        set2_label: int = self.find_set(label2)
        if set1_label == set2_label:
            return

        if self.set_sizes[set1_label] < self.set_sizes[set2_label]:
            small = set1_label
            large = set2_label
        else:
            small = set2_label
            large = set1_label
        self.nodes[small].parent = self.nodes[large]
        self.set_sizes[large] += self.set_sizes[small]
        self.set_sizes[small] = 0
        self.num_disjoint_sets -= 1

    def print_sets(self):
        """Display the current state of the UnionFind data structure."""
        for x in self.nodes:
            root = self.find_set(x)
            print(x, ": ", root)
