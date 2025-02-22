"""Code to create the Prisoners and Guards Puzzle from Chapter 6.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import math
import queue
from typing import Union

from graph_algorithms_the_fun_way.graph import Graph, Node
from graph_algorithms_the_fun_way.search import breadth_first_search


class PGState:
    """A data structure for holding the information about a single state
    in the Prisoners and Guards Puzzle.

    Attributes
    ----------
    guards_left : int
        The number of guards on the left shore.
    prisoners_left : int
        The number of prisoners on the left shore.
    boat_side : str
        The boat's side ("L" or "R")
    """

    def __init__(self, guards_left: int = 3, prisoners_left: int = 3, boat_side: str = "L"):
        self.guards_left = guards_left
        self.prisoners_left = prisoners_left
        self.boat_side = boat_side

    def __str__(self):
        return f"{self.guards_left},{self.prisoners_left},{self.boat_side}"

    def check_valid(self) -> bool:
        """Check if the current state is valid."""
        G_L: int = self.guards_left
        G_R: int = 3 - self.guards_left
        P_L: int = self.prisoners_left
        P_R: int = 3 - self.prisoners_left

        if G_L < 0 or G_R < 0 or P_L < 0 or P_R < 0:
            return False
        if G_L > 0 and G_L < P_L:
            return False
        if G_R > 0 and G_R < P_R:
            return False
        return True

    def check_transition_valid(self, state2):
        """Check if the transition between the current state
        and a second state is valid.

        Parameters
        ----------
        state2 : PGState
            The state to which the puzzle is moving.

        Returns
        -------
        bool
            Indicates whether the transition is valid.
        """
        if self.boat_side == state2.boat_side:
            return False
        if self.boat_side == "L":
            if self.guards_left < state2.guards_left:
                return False
            if self.prisoners_left < state2.prisoners_left:
                return False
            in_boat = state2.guards_left - self.guards_left + state2.prisoners_left - self.prisoners_left
            if in_boat > 2:
                return False
        else:
            if self.guards_left > state2.guards_left:
                return False
            if self.prisoners_left > state2.prisoners_left:
                return False
            in_boat = self.guards_left - state2.guards_left + self.prisoners_left - state2.prisoners_left
            if in_boat > 2:
                return False
        return True


def pg_result_of_move(state: PGState, num_guards: int, num_prisoners: int) -> Union[PGState, None]:
    """Compute the state that results from a move.

    Parameters
    ----------
    state : PGState
        The current state.
    num_guards : int
        The number of guards to move on the boat.
    num_prisoners : int
        The number of prisoners to move on the boat.

    Returns
    -------
    PGState or None
        If the move is valid, returns the new PGState. Otherwise returns None.
    """
    if num_guards < 0 or num_prisoners < 0:
        return None
    if num_guards + num_prisoners == 0:
        return None
    if num_guards + num_prisoners > 2:
        return None

    G_L: int = state.guards_left
    G_R: int = 3 - state.guards_left
    P_L: int = state.prisoners_left
    P_R: int = 3 - state.prisoners_left
    if state.boat_side == "L":
        G_L -= num_guards
        G_R += num_guards
        P_L -= num_prisoners
        P_R += num_prisoners
        new_side: str = "R"
    else:
        G_L += num_guards
        G_R -= num_guards
        P_L += num_prisoners
        P_R -= num_prisoners
        new_side = "L"

    if G_L < 0 or P_L < 0 or G_R < 0 or P_R < 0:
        return None

    if G_L > 0 and G_L < P_L:
        return None
    if G_R > 0 and G_R < P_R:
        return None
    return PGState(G_L, P_L, new_side)


def pg_neighbors(state: PGState) -> list:
    """Compute a list of all neighboring states for a given state.

    Parameters
    ----------
    state : PGState
        The current state.

    Returns
    -------
    neighbors : list of PGState
        The neighboring states that can be reached with a single valid move.
    """
    neighbors: list = []
    for move in [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]:
        n: Union[PGState, None] = pg_result_of_move(state, move[0], move[1])
        if n is not None:
            neighbors.append(n)
    return neighbors


def create_prisoners_and_guards() -> Graph:
    """Create a graph representing the Prisoners and Guards Puzzle.

    Returns
    -------
    g : Graph
        The graph representing the puzzle.
    """
    indices: dict = {}
    next_node: queue.Queue = queue.Queue()
    g: Graph = Graph(0, undirected=True)

    initial_state: PGState = PGState(3, 3, "L")
    initial: Node = g.insert_node(label=initial_state)
    next_node.put(initial.index)
    indices[str(initial_state)] = initial.index

    while not next_node.empty():
        current_ind: int = next_node.get()
        current_node: Node = g.nodes[current_ind]
        current_state = current_node.label

        neighbors: list = pg_neighbors(current_state)
        for state in neighbors:
            state_str: str = str(state)
            if not state_str in indices:
                new_node: Node = g.insert_node(label=state)
                indices[state_str] = new_node.index
                next_node.put(new_node.index)
            new_ind: int = indices[str(state)]
            g.insert_edge(current_ind, new_ind, 1.0)
    return g


def pg_state_to_index_map(g: Graph) -> dict:
    """Create a map of each state to the corresponding node's index.

    Parameters
    ----------
    g : Graph
        The graph representing the puzzle.

    Returns
    -------
    state_to_index : dict
        A dictionary mapping the state's string to node's index.
    """
    state_to_index: dict = {}
    for node in g.nodes:
        state: str = str(node.label)
        state_to_index[state] = node.index
    return state_to_index


def solve_pg_bfs():
    """Solve the Prisoners and Guards Puzzle using BFS."""
    g: Graph = create_prisoners_and_guards()

    state_to_index: dict = pg_state_to_index_map(g)
    start_index: int = state_to_index["3,3,L"]
    end_index: int = state_to_index["0,0,R"]

    last: int = breadth_first_search(g, start_index)

    current: int = end_index
    path_reversed: list = []
    while current != -1:
        path_reversed.append(current)
        current = last[current]

    if path_reversed[-1] != start_index:
        print("No solution")
        return

    for i, n in enumerate(reversed(path_reversed)):
        print(f"Step {i}: {g.nodes[n].label}")


def pg_generate_heuristic(g: Graph) -> list:
    """Generate the heuristic vector for the Prisoners and Guards Puzzle
    to use in A* search (Chapter 8).

    Parameters
    ----------
    g : Graph
        The graph representing the puzzle.

    Returns
    -------
    heuristic : list of float
        Maps each node's index to its heuristic value.
    """
    heuristic = [0.0] * g.num_nodes
    for node in g.nodes:
        state: PGState = node.label
        num_left: int = state.guards_left + state.prisoners_left
        min_trips_l_to_r: int = math.ceil(num_left / 2.0)
        min_trips_r_to_l: int = max(0, min_trips_l_to_r - 1)
        if not state.boat_side == "L" and min_trips_l_to_r > 0:
            min_trips_r_to_l += 1
        heuristic[node.index] = min_trips_l_to_r + min_trips_r_to_l

    return heuristic
