"""Algorithms for topological sort (Chapter 9)

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from graph_algorithms_the_fun_way.graph import Graph


def is_topo_ordered(g: Graph, ordering: list) -> bool:
    """Check if a topological ordering is valid.

    Parameters
    ----------
    g : Graph
        The input graph.
    ordering : list of int
        A list of node indices in order.

    Returns
    -------
    bool
        Whether the ordering is a valid topological ordering.
    """
    if len(ordering) != g.num_nodes:
        return False

    index_to_pos: list = [-1] * g.num_nodes
    for pos in range(g.num_nodes):
        current: int = ordering[pos]
        if index_to_pos[current] != -1:
            return False
        index_to_pos[current] = pos

    for n in g.nodes:
        for edge in n.get_edge_list():
            if index_to_pos[edge.to_node] <= index_to_pos[n.index]:
                return False
    return True


def Kahns(g: Graph) -> list:
    """Kahn's algorithm for topological sort.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    result : list of int
        A list of node indices in topological order.
    """
    count: list = [0] * g.num_nodes
    s: list = []
    result: list = []

    for current in g.nodes:
        for edge in current.get_edge_list():
            count[edge.to_node] = count[edge.to_node] + 1
    for current in g.nodes:
        if count[current.index] == 0:
            s.append(current.index)

    while len(s) > 0:
        current_index: int = s.pop()
        result.append(current_index)
        for edge in g.nodes[current_index].get_edge_list():
            count[edge.to_node] = count[edge.to_node] - 1
            if count[edge.to_node] == 0:
                s.append(edge.to_node)

    return result


def check_cycle_kahns(g: Graph) -> bool:
    """A function to checl whether the graph contains a cycle.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    bool
        True if the graph contains a cycle and False otherwise.
    """
    result: list = Kahns(g)
    if len(result) == g.num_nodes:
        return False
    return True


def topological_dfs(g: Graph) -> list:
    """Depth-first search for topological sort.

    Parameters
    ----------
    g : Graph
        The input graph.

    Returns
    -------
    result : list of int
        A list of node indices in topological order.
    """
    seen: list = [False] * g.num_nodes
    s: list = []
    for ind in range(g.num_nodes):
        if not seen[ind]:
            topological_dfs_recursive(g, ind, seen, s)
    s.reverse()
    return s


def topological_dfs_recursive(g: Graph, index: int, seen: list, s: list):
    """The recursive function for DFS topological sort.

    Parameters
    ----------
    g : Graph
        The input graph.
    index : int
        The current index.
    seen : list of bool
        Whether each node in the graph has been marked seen.
    s : list
        A list representing the stack.
    """
    seen[index] = True
    current: Node = g.nodes[index]
    for edge in current.get_edge_list():
        neighbor: int = edge.to_node
        if not seen[neighbor]:
            topological_dfs_recursive(g, neighbor, seen, s)
    s.append(index)


def sort_forward_pointers(options: list) -> list:
    """A function to sort forward pointers.

    Parameters
    ----------
    options : list of list of int
        The forward options at each node.

    Returns
    -------
    result : list of int
        A list of node indices in topological order.
    """
    num_nodes: int = len(options)
    g: Graph = Graph(num_nodes)
    for current in range(num_nodes):
        for next_index in options[current]:
            if next_index != -1:
                g.insert_edge(current, next_index, 1.0)
    return Kahns(g)
