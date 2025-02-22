"""Functions for reading in saved Graphs (Appendix A)

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import csv
from typing import Union

from graph_algorithms_the_fun_way.graph import Edge, Graph, Node


def make_graph_from_weighted_csv(filename: str, undirected: bool) -> Graph:
    """Read a graph from a (weighted) CSV file.

    Parameters
    ----------
    filename : str
        The name of the file to read.
    undirected : bool
        A Boolean indicating whether the graph is undirected (True) or
        directed (False).

    Returns
    -------
    g : Graph
        The loaded Graph.
    """
    g: Graph = Graph(0, undirected)
    node_indices: dict = {}

    with open(filename) as f:
        graph_reader = csv.reader(f, delimiter=",")
        for row in graph_reader:
            name1: str = row[0]
            if name1 not in node_indices:
                new_node: Node = g.insert_node(label=name1)
                node_indices[name1] = new_node.index
            index1: int = node_indices[name1]

            if len(row) > 1:
                name2: str = row[1]
                if name2 not in node_indices:
                    new_node = g.insert_node(label=name2)
                    node_indices[name2] = new_node.index
                index2: int = node_indices[name2]

                if len(row) > 2:
                    weight: float = float(row[2])
                else:
                    weight = 1.0

                g.insert_edge(index1, index2, weight)
    return g


def make_graph_from_weighted_csv2(filename: str, undirected: bool) -> Graph:
    """Read a graph from a (weighted) CSV file using the ability to insert nodes by name.

    Parameters
    ----------
    filename : str
        The name of the file to read.
    undirected : bool
        A Boolean indicating whether the graph is undirected (True) or
        directed (False).

    Returns
    -------
    g : Graph
        The loaded Graph.
    """
    g: Graph = Graph(0, undirected)

    with open(filename) as f:
        graph_reader = csv.reader(f, delimiter=",")
        for row in graph_reader:
            index1: int = g.get_index_by_name(row[0])

            if len(row) > 1:
                index2: int = g.get_index_by_name(row[1])

                if len(row) > 2:
                    weight: float = float(row[2])
                else:
                    weight = 1.0
                g.insert_edge(index1, index2, weight)
    return g


def save_graph_to_csv(g: Graph, filename: str):
    """Save a graph to a weighted CSV file.

    Parameters
    ----------
    g : Graph
        The Graph to save.
    filename : str
        The name of the file to which to write the graph.
    """
    with open(filename, "w", newline="\n") as f:
        graph_writer = csv.writer(f, delimiter=",")
        for node in g.nodes:
            graph_writer.writerow([node.index])

        for node in g.nodes:
            for edge in node.get_edge_list():
                graph_writer.writerow([edge.from_node, edge.to_node, edge.weight])


def make_graph_from_multi_csv(filename: str) -> Graph:
    """Read a graph a CSV with multiple node names per line (co-occurrence graph).

    Parameters
    ----------
    filename : str
        The name of the file to read.

    Returns
    -------
    g : Graph
        The loaded Graph.
    """
    g: Graph = Graph(0, undirected=True)
    with open(filename) as f:
        graph_reader = csv.reader(f, delimiter=",")
        for row in graph_reader:
            num_items: int = len(row)

            for i in range(num_items):
                index1: int = g.get_index_by_name(row[i])

                for j in range(i + 1, num_items):
                    index2: int = g.get_index_by_name(row[j])
                    edge: Union[Edge, None] = g.get_edge(index1, index2)
                    if edge is not None:
                        weight = edge.weight + 1.0
                    else:
                        weight = 1.0
                    g.insert_edge(index1, index2, weight)
    return g


def make_graph_from_dependencies(dependencies: dict) -> Graph:
    """Make a graph from node dependencies.

    Parameters
    ----------
    dependencies : dict
        A dictionary mapping each node index to a list of
        the nodes on which it depends.

    Returns
    -------
    g : Graph
        The constructed Graph.
    """
    g: Graph = Graph(0, undirected=False)
    for node in dependencies:
        n_index: int = g.get_index_by_name(node)
        for prior in dependencies[node]:
            p_index: int = g.get_index_by_name(prior)
            g.insert_edge(p_index, n_index, 1.0)
    return g
