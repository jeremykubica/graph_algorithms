import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.vertex_cover import *


class TestGraphVertexCover(unittest.TestCase):
    def setUp(self):
        """Create common test graphs."""
        self.g4 = Graph(4, undirected=True)
        self.g4.insert_edge(0, 1, 1.0)
        self.g4.insert_edge(0, 3, 1.0)
        self.g4.insert_edge(1, 2, 1.0)
        self.g4.insert_edge(1, 3, 1.0)

        self.g4b = Graph(4, undirected=True)
        self.g4b.insert_edge(0, 1, 1.0)
        self.g4b.insert_edge(0, 2, 1.0)
        self.g4b.insert_edge(1, 3, 1.0)

        self.g4_self = Graph(4, undirected=True)
        self.g4_self.insert_edge(0, 1, 1.0)
        self.g4_self.insert_edge(0, 3, 1.0)
        self.g4_self.insert_edge(1, 2, 1.0)
        self.g4_self.insert_edge(1, 3, 1.0)
        self.g4_self.insert_edge(3, 3, 1.0)

        self.g5 = Graph(5, undirected=True)
        self.g5.insert_edge(0, 1, 1.0)
        self.g5.insert_edge(0, 2, 1.0)
        self.g5.insert_edge(1, 2, 1.0)
        self.g5.insert_edge(1, 3, 1.0)
        self.g5.insert_edge(1, 4, 1.0)
        self.g5.insert_edge(2, 3, 1.0)
        self.g5.insert_edge(2, 4, 1.0)
        self.g5.insert_edge(3, 4, 1.0)

        self.g6 = Graph(6, undirected=True)
        self.g6.insert_edge(0, 1, 1.0)
        self.g6.insert_edge(1, 2, 1.0)
        self.g6.insert_edge(0, 3, 1.0)
        self.g6.insert_edge(3, 4, 1.0)
        self.g6.insert_edge(4, 5, 1.0)
        self.g6.insert_edge(1, 5, 1.0)
        self.g6.insert_edge(2, 5, 1.0)

    def test_is_vertex_cover_4(self):
        """Test is_vertex_cover on one of the graphs."""
        self.assertFalse(is_vertex_cover(self.g4, []))
        self.assertFalse(is_vertex_cover(self.g4, [0]))
        self.assertFalse(is_vertex_cover(self.g4, [1]))
        self.assertFalse(is_vertex_cover(self.g4, [2, 3]))
        self.assertFalse(is_vertex_cover(self.g4, [0, 2]))
        self.assertFalse(is_vertex_cover(self.g4, [1, 2]))

        self.assertTrue(is_vertex_cover(self.g4, [0, 1]))
        self.assertTrue(is_vertex_cover(self.g4, [0, 2, 3]))
        self.assertTrue(is_vertex_cover(self.g4, [0, 1, 2, 3]))
        self.assertTrue(is_vertex_cover(self.g4, [0, 1, 3]))

    def test_is_vertex_cover_4_self(self):
        """Test is_vertex_cover on one of the graphs."""
        self.assertFalse(is_vertex_cover(self.g4_self, []))
        self.assertFalse(is_vertex_cover(self.g4_self, [0]))
        self.assertFalse(is_vertex_cover(self.g4_self, [1]))
        self.assertFalse(is_vertex_cover(self.g4_self, [2, 3]))
        self.assertFalse(is_vertex_cover(self.g4_self, [0, 2]))
        self.assertFalse(is_vertex_cover(self.g4_self, [1, 2]))
        self.assertFalse(is_vertex_cover(self.g4_self, [0, 1]))

        self.assertTrue(is_vertex_cover(self.g4_self, [0, 2, 3]))
        self.assertTrue(is_vertex_cover(self.g4_self, [0, 1, 2, 3]))
        self.assertTrue(is_vertex_cover(self.g4_self, [0, 1, 3]))

    def test_is_vertex_cover_4b(self):
        """Test is_vertex_cover on one of the graphs."""
        self.assertFalse(is_vertex_cover(self.g4b, []))
        self.assertFalse(is_vertex_cover(self.g4b, [0]))
        self.assertFalse(is_vertex_cover(self.g4b, [1]))
        self.assertFalse(is_vertex_cover(self.g4b, [2, 3]))
        self.assertFalse(is_vertex_cover(self.g4b, [0, 2]))

        self.assertTrue(is_vertex_cover(self.g4b, [0, 1]))
        self.assertTrue(is_vertex_cover(self.g4b, [1, 2]))
        self.assertTrue(is_vertex_cover(self.g4b, [0, 2, 3]))

    def test_is_vertex_cover_5(self):
        """Test is_vertex_cover on one of the graphs."""
        self.assertFalse(is_vertex_cover(self.g5, []))
        self.assertFalse(is_vertex_cover(self.g5, [4]))
        self.assertFalse(is_vertex_cover(self.g5, [3]))
        self.assertFalse(is_vertex_cover(self.g5, [0, 3]))
        self.assertFalse(is_vertex_cover(self.g5, [0, 4]))
        self.assertFalse(is_vertex_cover(self.g5, [0, 2, 4]))

        self.assertTrue(is_vertex_cover(self.g5, [0, 1, 3, 4]))
        self.assertTrue(is_vertex_cover(self.g5, [1, 2, 3]))
        self.assertTrue(is_vertex_cover(self.g5, [1, 2, 4]))

    def test_is_vertex_cover_6(self):
        """Test is_vertex_cover on one of the graphs."""
        self.assertFalse(is_vertex_cover(self.g6, []))
        self.assertFalse(is_vertex_cover(self.g6, [1]))
        self.assertFalse(is_vertex_cover(self.g6, [5]))
        self.assertFalse(is_vertex_cover(self.g6, [0, 4]))
        self.assertFalse(is_vertex_cover(self.g6, [0, 2, 4]))
        self.assertFalse(is_vertex_cover(self.g6, [3, 5]))

        self.assertTrue(is_vertex_cover(self.g6, [0, 1, 4, 5]))
        self.assertTrue(is_vertex_cover(self.g6, [0, 2, 3, 5]))
        self.assertTrue(is_vertex_cover(self.g6, [1, 2, 3, 4]))

    def test_is_vertex_cover_greed_choice_4(self):
        """Test vertex_cover_greedy_choice on one of the graphs."""
        self.assertEqual(vertex_cover_greedy_choice(self.g4, []), 1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4, [1]), 0)
        self.assertEqual(vertex_cover_greedy_choice(self.g4, [0, 1]), -1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4, [2]), 0)
        self.assertEqual(vertex_cover_greedy_choice(self.g4, [3]), 1)

    def test_is_vertex_cover_greed_choice_4_self(self):
        """Test vertex_cover_greedy_choice on one of the graphs."""
        self.assertEqual(vertex_cover_greedy_choice(self.g4_self, []), 1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4_self, [1]), 3)
        self.assertEqual(vertex_cover_greedy_choice(self.g4_self, [0, 1]), 3)
        self.assertEqual(vertex_cover_greedy_choice(self.g4_self, [0, 1, 3]), -1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4_self, [1, 3]), -1)

    def test_is_vertex_cover_greed_choice_4b(self):
        """Test vertex_cover_greedy_choice on one of the graphs."""
        self.assertEqual(vertex_cover_greedy_choice(self.g4b, []), 0)
        self.assertEqual(vertex_cover_greedy_choice(self.g4b, [1]), 0)
        self.assertEqual(vertex_cover_greedy_choice(self.g4b, [0, 1]), -1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4b, [2]), 1)
        self.assertEqual(vertex_cover_greedy_choice(self.g4b, [0]), 1)

    def test_is_vertex_cover_greed_choice_5(self):
        """Test vertex_cover_greedy_choice on one of the graphs."""
        self.assertEqual(vertex_cover_greedy_choice(self.g5, []), 1)
        self.assertEqual(vertex_cover_greedy_choice(self.g5, [1]), 2)
        self.assertEqual(vertex_cover_greedy_choice(self.g5, [0, 1]), 2)
        self.assertEqual(vertex_cover_greedy_choice(self.g5, [1, 2]), 3)
        self.assertEqual(vertex_cover_greedy_choice(self.g5, [1, 2, 3]), -1)
        self.assertEqual(vertex_cover_greedy_choice(self.g5, [0, 4]), 1)

    def test_is_vertex_cover_greed_choice_6(self):
        """Test vertex_cover_greedy_choice on one of the graphs."""
        self.assertEqual(vertex_cover_greedy_choice(self.g6, []), 1)
        self.assertEqual(vertex_cover_greedy_choice(self.g6, [1]), 3)
        self.assertEqual(vertex_cover_greedy_choice(self.g6, [1, 3]), 5)
        self.assertEqual(vertex_cover_greedy_choice(self.g6, [1, 3, 5]), -1)
        self.assertEqual(vertex_cover_greedy_choice(self.g6, [1, 2, 3]), 4)
        self.assertEqual(vertex_cover_greedy_choice(self.g6, [0, 4, 5]), 1)

    def test_vertex_cover_greedy_greedy_4(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(vertex_cover_greedy(self.g4), [1, 0])

    def test_vertex_cover_greedy_4b(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(vertex_cover_greedy(self.g4b), [0, 1])

    def test_vertex_cover_greedy_5(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(vertex_cover_greedy(self.g5), [1, 2, 3])

    def test_vertex_cover_greedy_6(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(vertex_cover_greedy(self.g6), [1, 3, 5])

    def test_vertex_cover_greedy_7(self):
        """Test greedy search on one of the graphs."""
        g7 = Graph(7, undirected=True)
        g7.insert_edge(0, 1, 1.0)
        g7.insert_edge(1, 2, 1.0)
        g7.insert_edge(2, 3, 1.0)
        g7.insert_edge(2, 5, 1.0)
        g7.insert_edge(3, 4, 1.0)
        g7.insert_edge(5, 6, 1.0)
        self.assertEqual(vertex_cover_greedy(g7), [2, 0, 3, 5])

    def test_minimum_vertex_cover_4(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(minimum_vertex_cover_backtracking(self.g4), [0, 1])

    def test_minimum_vertex_cover_4b(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(minimum_vertex_cover_backtracking(self.g4b), [0, 1])

    def test_minimum_vertex_cover_5(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(minimum_vertex_cover_backtracking(self.g5), [1, 2, 3])

    def test_minimum_vertex_cover_6(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(minimum_vertex_cover_backtracking(self.g6), [1, 3, 5])

    def test_minimum_vertex_cover_7(self):
        """Test backtracking search on one of the graphs."""
        g7 = Graph(7, undirected=True)
        g7.insert_edge(0, 1, 1.0)
        g7.insert_edge(1, 2, 1.0)
        g7.insert_edge(2, 3, 1.0)
        g7.insert_edge(2, 5, 1.0)
        g7.insert_edge(3, 4, 1.0)
        g7.insert_edge(5, 6, 1.0)

        self.assertEqual(minimum_vertex_cover_backtracking(g7), [1, 3, 5])


if __name__ == "__main__":
    unittest.main()
