import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.topological import (
    check_cycle_kahns,
    is_topo_ordered,
    Kahns,
    sort_forward_pointers,
    topological_dfs,
)


class TestGraphTopological(unittest.TestCase):
    def setUp(self):
        """Set up graphs to use for the tests."""
        self.g_line = Graph(4, undirected=False)
        self.g_line.insert_edge(1, 0, 1.0)
        self.g_line.insert_edge(0, 3, 1.0)
        self.g_line.insert_edge(3, 2, 1.0)
        self.g_line_result = [1, 0, 3, 2]

        self.g_line2 = Graph(4, undirected=False)
        self.g_line2.insert_edge(1, 0, 1.0)
        self.g_line2.insert_edge(0, 2, 1.0)
        self.g_line2.insert_edge(3, 2, 1.0)
        self.g_line2_result = [3, 1, 0, 2]

        self.g_y = Graph(4, undirected=False)
        self.g_y.insert_edge(1, 0, 1.0)
        self.g_y.insert_edge(0, 3, 1.0)
        self.g_y.insert_edge(2, 0, 1.0)
        self.g_y.insert_edge(2, 3, 1.0)
        self.g_y_result_k = [2, 1, 0, 3]
        self.g_y_result_d = [1, 2, 0, 3]

        # This is the graph from figures 9-5 and 9-6.
        self.g6 = Graph(6, undirected=False)
        self.g6.insert_edge(0, 2, 1.0)
        self.g6.insert_edge(0, 3, 1.0)
        self.g6.insert_edge(2, 4, 1.0)
        self.g6.insert_edge(3, 4, 1.0)
        self.g6.insert_edge(4, 5, 1.0)
        self.g6.insert_edge(1, 3, 1.0)
        self.g6.insert_edge(1, 4, 1.0)
        self.g6_result = [1, 0, 3, 2, 4, 5]

        self.g6b = Graph(6, undirected=False)
        self.g6b.insert_edge(0, 1, 1.0)
        self.g6b.insert_edge(0, 2, 1.0)
        self.g6b.insert_edge(0, 3, 1.0)
        self.g6b.insert_edge(2, 4, 1.0)
        self.g6b.insert_edge(4, 3, 1.0)
        self.g6b.insert_edge(3, 5, 1.0)
        self.g6b.insert_edge(5, 1, 1.0)
        self.g6b_result = [0, 2, 4, 3, 5, 1]

        self.g8 = Graph(8, undirected=False)
        self.g8.insert_edge(0, 4, 1.0)
        self.g8.insert_edge(1, 2, 1.0)
        self.g8.insert_edge(1, 3, 1.0)
        self.g8.insert_edge(1, 5, 1.0)
        self.g8.insert_edge(2, 0, 1.0)
        self.g8.insert_edge(2, 4, 1.0)
        self.g8.insert_edge(3, 5, 1.0)
        self.g8.insert_edge(3, 6, 1.0)
        self.g8.insert_edge(4, 3, 1.0)
        self.g8.insert_edge(7, 5, 1.0)
        self.g8.insert_edge(7, 6, 1.0)
        self.g8_result = [7, 1, 2, 0, 4, 3, 6, 5]

    def test_kahns(self):
        """Test Kahn's algorithm."""
        result = Kahns(self.g_line)
        for i in range(len(self.g_line_result)):
            self.assertEqual(result[i], self.g_line_result[i])

        result = Kahns(self.g_y)
        for i in range(len(self.g_y_result_k)):
            self.assertEqual(result[i], self.g_y_result_k[i])

        result = Kahns(self.g6b)
        for i in range(len(self.g6b_result)):
            self.assertEqual(result[i], self.g6b_result[i])

        # Test Figure 9-5.
        result = Kahns(self.g6)
        for i in range(len(self.g6_result)):
            self.assertEqual(result[i], self.g6_result[i])

        result = Kahns(self.g8)
        for i in range(len(self.g8_result)):
            self.assertEqual(result[i], self.g8_result[i])

    def test_dfs(self):
        """Test DFS for topological sort."""
        result = topological_dfs(self.g_line)
        for i in range(len(self.g_line_result)):
            self.assertEqual(result[i], self.g_line_result[i])

        result = topological_dfs(self.g_line2)
        for i in range(len(self.g_line2_result)):
            self.assertEqual(result[i], self.g_line2_result[i])

        result = topological_dfs(self.g_y)
        for i in range(len(self.g_y_result_k)):
            self.assertEqual(result[i], self.g_y_result_k[i])

        result = topological_dfs(self.g6b)
        for i in range(len(self.g6b_result)):
            self.assertEqual(result[i], self.g6b_result[i])

        # Test Figure 9-6.
        result = topological_dfs(self.g6)
        for i in range(len(self.g6_result)):
            self.assertEqual(result[i], self.g6_result[i])

        result = topological_dfs(self.g8)
        for i in range(len(self.g8_result)):
            self.assertEqual(result[i], self.g8_result[i])

    def test_cycle_check_kahns(self):
        """Test that we can use Kahn's algorithm to detect cycles."""
        self.assertEqual(check_cycle_kahns(self.g_line), False)
        self.g_line.insert_edge(2, 0, 1.0)
        self.assertEqual(check_cycle_kahns(self.g_line), True)

        self.assertEqual(check_cycle_kahns(self.g_y), False)
        self.g_y.insert_edge(3, 1, 1.0)
        self.assertEqual(check_cycle_kahns(self.g_y), True)

        self.assertEqual(check_cycle_kahns(self.g6b), False)
        self.g6b.insert_edge(3, 1, 1.0)
        self.assertEqual(check_cycle_kahns(self.g6b), False)
        self.g6b.insert_edge(4, 2, 1.0)
        self.assertEqual(check_cycle_kahns(self.g6b), True)

        self.assertEqual(check_cycle_kahns(self.g6), False)
        self.g6.insert_edge(2, 1, 1.0)
        self.assertEqual(check_cycle_kahns(self.g6), False)
        self.g6.insert_edge(3, 2, 1.0)
        self.assertEqual(check_cycle_kahns(self.g6), True)

        self.assertEqual(check_cycle_kahns(self.g8), False)
        self.g8.insert_edge(5, 6, 1.0)
        self.assertEqual(check_cycle_kahns(self.g8), False)
        self.g8.insert_edge(2, 3, 1.0)
        self.assertEqual(check_cycle_kahns(self.g8), False)
        self.g8.insert_edge(6, 4, 1.0)
        self.assertEqual(check_cycle_kahns(self.g8), True)

        g_disconnected = Graph(5, undirected=False)
        g_disconnected.insert_edge(0, 1, 1.0)
        g_disconnected.insert_edge(3, 2, 1.0)
        self.assertEqual(check_cycle_kahns(g_disconnected), False)

        g_ring = Graph(6, undirected=False)
        g_ring.insert_edge(0, 1, 1.0)
        g_ring.insert_edge(1, 2, 1.0)
        g_ring.insert_edge(2, 3, 1.0)
        g_ring.insert_edge(3, 4, 1.0)
        g_ring.insert_edge(4, 5, 1.0)
        self.assertEqual(check_cycle_kahns(g_ring), False)
        g_ring.insert_edge(5, 0, 1.0)
        self.assertEqual(check_cycle_kahns(g_ring), True)

    def test_is_topo_ordered(self):
        """Test the is_topo_ordered() check."""
        self.assertEqual(True, is_topo_ordered(self.g_line, self.g_line_result))
        self.assertEqual(False, is_topo_ordered(self.g_line, [2, 0, 3, 1]))
        self.assertEqual(False, is_topo_ordered(self.g_line, []))
        self.assertEqual(False, is_topo_ordered(self.g_line, [2, 0, 3, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_line, [2, 0, 1, 3]))
        self.assertEqual(False, is_topo_ordered(self.g_line, [0, 1, 3, 2]))

        self.assertEqual(True, is_topo_ordered(self.g_line2, self.g_line2_result))
        self.assertEqual(False, is_topo_ordered(self.g_line2, [2, 0, 3, 1]))
        self.assertEqual(False, is_topo_ordered(self.g_line2, [3, 0, 1, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_line2, [2, 0, 3, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_line2, [2, 0, 1, 3]))
        self.assertEqual(False, is_topo_ordered(self.g_line2, [0, 1, 3, 2]))

        self.assertEqual(True, is_topo_ordered(self.g_y, self.g_y_result_k))
        self.assertEqual(True, is_topo_ordered(self.g_y, self.g_y_result_d))
        self.assertEqual(False, is_topo_ordered(self.g_y, [2, 0, 3, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_y, [2, 0, 1, 3]))
        self.assertEqual(False, is_topo_ordered(self.g_y, [0, 1, 3, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_y, [3, 0, 1, 2]))
        self.assertEqual(False, is_topo_ordered(self.g_y, [1, 2, 3, 0]))

        self.assertEqual(True, is_topo_ordered(self.g6b, self.g6b_result))
        self.assertEqual(False, is_topo_ordered(self.g6b, [0, 2, 3, 4, 5, 1]))
        self.assertEqual(False, is_topo_ordered(self.g6b, [0, 2, 4, 3, 1, 5]))
        self.assertEqual(False, is_topo_ordered(self.g6b, [0, 2, 4, 3, 5]))
        self.assertEqual(False, is_topo_ordered(self.g6b, [1, 0, 2, 3, 5, 4]))
        self.assertEqual(False, is_topo_ordered(self.g6b, [1, 0, 5, 2, 3, 4]))

        self.assertEqual(True, is_topo_ordered(self.g6, self.g6_result))

        self.assertEqual(True, is_topo_ordered(self.g8, self.g8_result))
        self.assertEqual(True, is_topo_ordered(self.g8, [1, 7, 2, 0, 4, 3, 6, 5]))
        self.assertEqual(False, is_topo_ordered(self.g8, [7, 3, 2, 0, 4, 1, 6, 5]))
        self.assertEqual(False, is_topo_ordered(self.g8, [7, 1, 2, 0, 4, 6, 3, 5]))
        self.assertEqual(False, is_topo_ordered(self.g8, [0, 1, 2, 4, 6, 7, 5, 3]))
        self.assertEqual(False, is_topo_ordered(self.g8, [2, 1, 7, 0, 4, 6, 3, 5]))

    def test_sort_forward_pointers(self):
        """Test that we can sort forward pointers."""
        # Build graph from Figure 9-11.
        options = [[1], [2], [4, 6], [-1], [5], [3, 8], [7], [-1], [9], [-1]]
        order = sort_forward_pointers(options)
        self.assertEqual(order, [0, 1, 2, 6, 7, 4, 5, 8, 9, 3])


if __name__ == "__main__":
    unittest.main()
