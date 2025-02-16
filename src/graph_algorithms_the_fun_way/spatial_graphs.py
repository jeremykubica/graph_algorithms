"""Helper functions for generating graphs from spatial data (Chapter 10)
and performing single linkage clustering (Chapter 10).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import math

from graph_algorithms_the_fun_way.union_find import UnionFind
from graph_algorithms_the_fun_way.graph import Graph


# -------------------------------------------------------
# --- Spatial Graph Construction ------------------------
# -------------------------------------------------------


class Point:
    """A data structure to represent a 2-d point.

    Attributes
    ----------
    x : float
        The x coordinate.
    y : float
        The y coordinate.
    """

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def distance(self, b) -> float:
        """Compute the Euclidean distance between the current point and another point.

        Parameters
        ----------
        b : Point
            The point to which to compute the distance.

        Returns
        -------
        dist : float
            The Euclidean distance.
        """
        diff_x: float = self.x - b.x
        diff_y: float = self.y - b.y
        dist: float = math.sqrt(diff_x * diff_x + diff_y * diff_y)
        return dist


def build_graph_from_points(points: list) -> Graph:
    """Construct a graph from a list of Points.

    Parameters
    ----------
    points : list of Point
        The spatial points.

    Returns
    -------
    g : Graph
        The constructed Graph.
    """
    num_pts: int = len(points)
    g: Graph = Graph(num_pts, undirected=True)

    for i in range(num_pts):
        for j in range(i + 1, num_pts):
            dist: float = points[i].distance(points[j])
            g.insert_edge(i, j, dist)
    return g


# -------------------------------------------------------
# --- Single-linkage Clustering -------------------------
# -------------------------------------------------------


class Link:
    """A link in single-linkage clustering.

    Attributes
    ----------
    dist : float
        The distance between two points.
    id1 : int
        The index of the first point.
    id2 : int
        The index of the second point.
    """

    def __init__(self, dist: float, id1: int, id2: int):
        self.dist: float = dist
        self.id1: int = id1
        self.id2: int = id2


def single_linkage_clustering(points: list) -> list:
    """Perform single-linkage clustering from a list of spatial points.

    Parameters
    ----------
    points : list of Point
        The spatial points.

    Returns
    -------
    cluster_links : list of Link
        The linkages in the clustering.
    """
    num_pts: int = len(points)
    djs: UnionFind = UnionFind(num_pts)
    all_links: list = []
    cluster_links: list = []

    for id1 in range(num_pts):
        for id2 in range(id1 + 1, num_pts):
            dist = points[id1].distance(points[id2])
            all_links.append(Link(dist, id1, id2))

    all_links.sort(key=lambda link: link.dist)

    for x in all_links:
        if djs.are_disjoint(x.id1, x.id2):
            cluster_links.append(x)
            djs.union_sets(x.id1, x.id2)

    return cluster_links
