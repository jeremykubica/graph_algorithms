"""Code to perform a dynamic A* search from chapter 8.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

import math

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.priorityqueue import PriorityQueue


class World:
    """A data structure for representing the world with which A* will interact.

    Attributes
    ----------
    g : Graph
        The input graph. The search does not see this directly.
    start_ind : int
        The index of the starting node.
    goal_ind : int
        The index of the goal node.
    """

    def __init__(self, g: Graph, start_ind: int, goal_ind: int):
        self.g = g
        self.start_ind = start_ind
        self.goal_ind = goal_ind

    def get_num_states(self) -> int:
        """Get the number of states in the world."""
        return self.g.num_nodes

    def is_goal(self, state: int) -> bool:
        """Check whether the current state is the goal.

        Parameters
        ----------
        state : int
            The index of the current state.

        Returns
        -------
        bool
            True if the state is the goal and False otherwise.
        """
        return state == self.goal_ind

    def get_start_index(self) -> int:
        """Get the index of the starting state."""
        return self.start_ind

    def get_neighbors(self, state: int) -> set:
        """Get all of the neighbors of the current state.

        Parameters
        ----------
        state : int
            The index of the current state.

        Returns
        -------
        set of int
            The indices of the neighboring states.
        """
        return self.g.nodes[state].get_neighbors()

    def get_cost(self, from_state: int, to_state: int) -> float:
        """Get the cost of transitioning between two states.

        Parameters
        ----------
        from_state : int
            The origin state.
        to_state : int
            The destination state.

        Returns
        -------
        float
            The cost.
        """
        if not self.g.is_edge(from_state, to_state):
            return math.inf
        return self.g.get_edge(from_state, to_state).weight

    def get_heuristic(self, state: int) -> float:
        """Get the heuristic value for a given state.

        Parameters
        ----------
        state : int
            The index of the current state.

        Returns
        -------
        float
            The heuristic value for this state.
        """
        pos1 = self.g.nodes[state].label
        pos2 = self.g.nodes[self.goal_ind].label
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def astar_dynamic(w: World):
    """The A* algorithm for exploring a world.

    Parameters
    ----------
    w : World
        The World object.

    Returns
    -------
    last : list of int
        The previous node's index for each node on the path.
    """
    visited: dict = {}
    last: dict = {}
    cost: dict = {}
    pq: PriorityQueue = PriorityQueue(min_heap=True)
    visited_goal: bool = False

    start: int = w.get_start_index()
    visited[start] = False
    last[start] = -1
    cost[start] = 0.0
    pq.enqueue(start, w.get_heuristic(start))

    while not pq.is_empty() and not visited_goal:
        index: int = pq.dequeue()
        visited[index] = True
        visited_goal = w.is_goal(index)

        for other in w.get_neighbors(index):
            c: float = w.get_cost(index, other)
            h: float = w.get_heuristic(other)

            if other not in visited:
                visited[other] = False
                last[other] = index
                cost[other] = cost[index] + c
                pq.enqueue(other, cost[other] + h)
            elif cost[other] > cost[index] + c:
                last[other] = index
                cost[other] = cost[index] + c
                pq.update_priority(other, cost[other] + h)

    return last
