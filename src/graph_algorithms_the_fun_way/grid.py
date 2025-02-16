"""Helper functions for making grid-based graphs (Chapter 5).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from graph_algorithms_the_fun_way.graph import Graph


def make_grid_graph(width: int, height: int) -> Graph:
    """Make a graph representing a rectangular grid.

    Parameters
    ----------
    width : int
        The width of the grid.
    height : int
        The height of the grid.

    Returns
    -------
    g : Graph
        The constructed Graph.
    """
    num_nodes: int = width * height

    g: Graph = Graph(num_nodes, undirected=True)
    for r in range(height):
        for c in range(width):
            index: int = r * width + c

            if c < width - 1:
                g.insert_edge(index, index + 1, 1.0)
            if r < height - 1:
                g.insert_edge(index, index + width, 1.0)
    return g


def make_grid_with_obstacles(width: int, height: int, obstacles: set) -> Graph:
    """Make a graph representing a rectangular grid with obstacles.

    Parameters
    ----------
    width : int
        The width of the grid.
    height : int
        The height of the grid.
    obstacles : set
        A set of (x, y) tuples indicating the location of obstacles.

    Returns
    -------
    g : Graph
        The constructed Graph.
    """
    num_nodes: int = width * height

    g: Graph = Graph(num_nodes, undirected=True)
    for r in range(height):
        for c in range(width):
            if (r, c) not in obstacles:
                index: int = r * width + c
                if (c < width - 1) and (r, c + 1) not in obstacles:
                    g.insert_edge(index, index + 1, 1.0)
                if (r < height - 1) and (r + 1, c) not in obstacles:
                    g.insert_edge(index, index + width, 1.0)
                g.label_node(index, f"{r:03d}_{c:03d}")
            else:
                index = width * r + c
                g.label_node(index, "Blocked")
    return g
