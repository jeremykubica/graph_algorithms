"""Algorithms for connect components including bridges (chapter 11),
articulation points (chapter 11), and strongly connected components
(chapter 12).

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import queue

from graph_algorithms_the_fun_way.graph import Graph, make_transpose_graph
from graph_algorithms_the_fun_way.search import dfs_connected_components


def get_reachable(g: Graph, index: int) -> set:
    """Retrieve the set of nodes that are reachable from a given node.

    Parameters
    ----------
    g : Graph
        The input graph.
    index : int
        The index of the query node.

    Returns
    -------
    seen : set of int
        The set of nodes that are reachable from a given node.
    """
    seen: set = set()
    pending: queue.Queue = queue.Queue()

    seen.add(index)
    pending.put(index)

    while not pending.empty():
        current_index: int = pending.get()
        current: Node = g.nodes[current_index]
        for edge in current.get_edge_list():
            neighbor: int = edge.to_node
            if neighbor not in seen:
                pending.put(neighbor)
                seen.add(neighbor)

    return seen


def check_strongly_connected(g: Graph, inds: list) -> bool:
    """A brute-force check if a list of nodes are strongly connected.

    Parameters
    ----------
    g : Graph
        The input graph.
    inds : list of int
        The node indices to check.

    Returns
    -------
    bool
        True if all the nodes are strongly connected and False otherwise.
    """
    for i in inds:
        reachable = get_reachable(g, i)
        for other in inds:
            if other not in reachable:
                return False
    return True


def add_reachable(g: Graph, index: int, seen: list, reachable: list):
    """Add all nodes reachable from a given node to a list in order of increasing finish time.

    Parameters
    ----------
    g : Graph
        The input graph.
    index : int
        The index of the current node.
    seen : list of bool
        Whether each node in the graph has been marked seen.
    reachable : int
        The current list of the reachable nodes' indices.
    """
    seen[index] = True
    current = g.nodes[index]

    for edge in current.get_edge_list():
        if not seen[edge.to_node]:
            add_reachable(g, edge.to_node, seen, reachable)
    reachable.append(index)


def kosaraju_sharir(g: Graph) -> list:
    """The Kosaraju-Sharir algorithm for strongly connected components.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    components : list of list of int
        The strongly connected components.
    """
    seen1: list = [False] * g.num_nodes
    finish_ordered: list = []
    for ind in range(g.num_nodes):
        if not seen1[ind]:
            add_reachable(g, ind, seen1, finish_ordered)

    gT: Graph = make_transpose_graph(g)

    seen2: list = [False] * g.num_nodes
    components: list = []
    while finish_ordered:
        start: int = finish_ordered.pop()
        if not seen2[start]:
            new_component: list = []
            add_reachable(gT, start, seen2, new_component)
            components.append(new_component)

    return components


class DFSTreeStats:
    """A data structure for collecting statistics during a depth-first search.

    Attributes
    ----------
    parent : list
        The index of the parent node for each node in the graph.
    next_order_index : int
        The next order index to assign.
    order : list
        Maps each node's index to its order index.
    lowest : list
        Maps each node's index to the lowest order index of any nodes
        in the DFS or their immediate neighbors.

    Parameters
    ----------
    num_nodes : int
        The number of nodes in the graph.
    """

    def __init__(self, num_nodes: int):
        self.parent: list = [-1] * num_nodes
        self.next_order_index: int = 0
        self.order: list = [-1] * num_nodes
        self.lowest: list = [-1] * num_nodes

    def set_order_index(self, node_index: int):
        """Sets the order index of a given node.

        Parameters
        ----------
        node_index : int
            The index of the node to set.
        """
        self.order[node_index] = self.next_order_index
        self.next_order_index += 1
        self.lowest[node_index] = self.order[node_index]

    def print_table(self):
        """Print a user readable version of the DFS stats."""
        print("Ind | Num | Low | Par")
        for v in range(len(self.lowest)):
            print("%3i | %3i | %3i | %3i" % (v, self.order[v], self.lowest[v], self.parent[v]))


def bridge_finding_dfs(g: Graph, index: int, stats: DFSTreeStats, results: list):
    """The recursive function for the bridge finding algorithm.

    Parameters
    ----------
    g : Graph
        The input graph.
    index : int
        The index of the current node.
    stats : DFSTreeStats
        The statistics from the search so far.
    results : list of Edge
        A list of all bridges found so far.
    """
    stats.set_order_index(index)

    for edge in g.nodes[index].get_sorted_edge_list():
        neighbor: int = edge.to_node
        if stats.order[neighbor] == -1:
            stats.parent[neighbor] = index
            bridge_finding_dfs(g, neighbor, stats, results)
            stats.lowest[index] = min(stats.lowest[index], stats.lowest[neighbor])
            if stats.lowest[neighbor] >= stats.order[neighbor]:
                results.append(edge)
        elif neighbor != stats.parent[index]:
            stats.lowest[index] = min(stats.lowest[index], stats.order[neighbor])


def find_bridges(g: Graph) -> list:
    """The outer function for the bridge finding algorithm.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    results : list of Edge
        A list of all bridges found.
    """
    results: list = []
    stats: DFSTreeStats = DFSTreeStats(g.num_nodes)
    for index in range(g.num_nodes):
        if stats.order[index] == -1:
            bridge_finding_dfs(g, index, stats, results)
    return results


def find_bridges_exh(g: Graph) -> list:
    """An exhaustive iterative search for finding bridges (for testing).

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    results : list of Edge
        A list of all bridges found.
    """
    num_comp = max(dfs_connected_components(g)) + 1
    all_edges = g.make_edge_list()

    results = []
    for edge in all_edges:
        if edge.to_node < edge.from_node:
            continue

        g.remove_edge(edge.from_node, edge.to_node)
        new_comp = max(dfs_connected_components(g)) + 1
        g.insert_edge(edge.from_node, edge.to_node, 1.0)

        if new_comp > num_comp:
            results.append(edge)

    return results


def articulation_point_dfs(g: Graph, index: int, stats: DFSTreeStats, results: set):
    """The recursive function for the articulation point finding algorithm.

    Parameters
    ----------
    g : Graph
        The input graph.
    index : int
        The index of the current node.
    stats : DFSTreeStats
        The statistics from the search so far.
    results : set of int
        A set of all articulation points found so far.
    """
    stats.set_order_index(index)
    for edge in g.nodes[index].get_edge_list():
        neighbor: int = edge.to_node
        if stats.order[neighbor] == -1:
            stats.parent[neighbor] = index
            articulation_point_dfs(g, neighbor, stats, results)
            stats.lowest[index] = min(stats.lowest[index], stats.lowest[neighbor])

            if stats.lowest[neighbor] >= stats.order[index]:
                results.add(index)

        elif neighbor != stats.parent[index]:
            stats.lowest[index] = min(stats.lowest[index], stats.order[neighbor])


def articulation_point_root(g: Graph, root: int, stats: DFSTreeStats, results: set):
    """The inner function for the articulation point finding algorithm at the root node.

    Parameters
    ----------
    g : Graph
        The input graph.
    root : int
        The index of the root node.
    stats : DFSTreeStats
        The statistics from the search so far.
    results : set of int
        A set of all articulation points found so far.
    """
    stats.set_order_index(root)
    num_subtrees: int = 0

    for edge in g.nodes[root].get_edge_list():
        neighbor: int = edge.to_node
        if stats.order[neighbor] == -1:
            stats.parent[neighbor] = root
            articulation_point_dfs(g, neighbor, stats, results)
            num_subtrees += 1

    if num_subtrees >= 2:
        results.add(root)


def find_articulation_points(g: Graph) -> set:
    """The outer function for the articulation point finding algorithm.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    results : set of int
        A set of all articulation points found.
    """
    stats: DFSTreeStats = DFSTreeStats(g.num_nodes)
    results: set = set()
    for index in range(g.num_nodes):
        if stats.order[index] == -1:
            articulation_point_root(g, index, stats, results)
    return results


def find_articulation_points_exh(g: Graph) -> list:
    """An exhaustive iterative search for finding articulation points (for testing).

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    results : list of int
        A list of all articulation points found.
    """
    comp_org = dfs_connected_components(g)

    results = []
    for i in range(g.num_nodes):
        gc = g.make_copy()

        # Instead of remove the node, just remove all its edges.
        for edge in g.nodes[i].get_edge_list():
            gc.remove_edge(edge.from_node, edge.to_node)

        # Use +1 here because the isolated node will be a sep component too.
        new_comp = dfs_connected_components(gc)
        if max(new_comp) > max(comp_org) + 1:
            results.append(i)

    return results
