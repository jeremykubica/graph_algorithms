import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.puzzles import *
from graph_algorithms_the_fun_way.search import astar_search, breadth_first_search


class TestPuzzles(unittest.TestCase):
    def test_create_prisoners_and_guards(self):
        """Test creating the puzzle."""
        g = create_prisoners_and_guards()

        # Check all the nodes are valid states.
        for node in g.nodes:
            state = node.label
            self.assertTrue(state.check_valid())

            for edge in node.get_edge_list():
                neighbor_ind = edge.to_node
                neighbor_node = g.nodes[neighbor_ind]
                neighbor_state = neighbor_node.label
                self.assertTrue(state.check_transition_valid(neighbor_state))

    def test_bsf_pg(self):
        """Test solving the puzzle with BFS."""
        g = create_prisoners_and_guards()

        # Build a dictionary of node state to index.
        state_to_index = pg_state_to_index_map(g)

        # Do the BFS
        last = breadth_first_search(g, 0)

        # Test the result
        self.assertEqual(last, [-1, 0, 0, 0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 14])

    def test_bsf_pg_funct(self):
        """Test solving the puzzle with solve_pg_bfs()."""
        solve_pg_bfs()
        self.assertTrue(True)

    def test_heuristic(self):
        """Test the generation of a heuristic and solving the puzzle with A*."""
        g: Graph = create_prisoners_and_guards()
        h: list = pg_generate_heuristic(g)
        true_dist = [11, 12, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0, 1]
        for i in range(g.num_nodes):
            self.assertLessEqual(h[i], true_dist[i])
        last: list = astar_search(g, h, 0, 14)


if __name__ == "__main__":
    unittest.main()
