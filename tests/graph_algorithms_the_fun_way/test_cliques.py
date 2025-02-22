import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.cliques import *


class TestGraphCliques(unittest.TestCase):
    def setUp(self):
        """Create common test graphs."""
        self.g4 = Graph(4, undirected=True)
        self.g4.insert_edge(0, 1, 1.0)
        self.g4.insert_edge(0, 3, 1.0)
        self.g4.insert_edge(1, 2, 1.0)
        self.g4.insert_edge(1, 3, 1.0)

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

        self.g8 = Graph(8, undirected=True)
        self.g8.insert_edge(0, 1, 1.0)
        self.g8.insert_edge(0, 3, 1.0)
        self.g8.insert_edge(1, 2, 1.0)
        self.g8.insert_edge(2, 4, 1.0)
        self.g8.insert_edge(2, 5, 1.0)
        self.g8.insert_edge(3, 4, 1.0)
        self.g8.insert_edge(3, 6, 1.0)
        self.g8.insert_edge(3, 7, 1.0)
        self.g8.insert_edge(4, 5, 1.0)
        self.g8.insert_edge(4, 6, 1.0)
        self.g8.insert_edge(4, 7, 1.0)
        self.g8.insert_edge(5, 7, 1.0)
        self.g8.insert_edge(6, 7, 1.0)

    def test_is_clique_4(self):
        """Test is_clique on one of the graphs."""
        self.assertTrue(is_clique(self.g4, []))
        self.assertTrue(is_clique(self.g4, [0]))
        self.assertTrue(is_clique(self.g4, [1]))
        self.assertTrue(is_clique(self.g4, [0, 1]))
        self.assertTrue(is_clique(self.g4, [1, 3]))
        self.assertTrue(is_clique(self.g4, [2, 1]))
        self.assertTrue(is_clique(self.g4, [0, 1, 3]))

        self.assertFalse(is_clique(self.g4, [0, 1, 2]))
        self.assertFalse(is_clique(self.g4, [0, 2]))
        self.assertFalse(is_clique(self.g4, [2, 3]))
        self.assertFalse(is_clique(self.g4, [1, 2, 3]))

    def test_is_clique_4_self(self):
        """Test is_clique on one of the graphs."""
        self.assertTrue(is_clique(self.g4_self, []))
        self.assertTrue(is_clique(self.g4_self, [0]))
        self.assertTrue(is_clique(self.g4_self, [1]))
        self.assertTrue(is_clique(self.g4_self, [0, 1]))
        self.assertTrue(is_clique(self.g4_self, [1, 3]))
        self.assertTrue(is_clique(self.g4_self, [2, 1]))
        self.assertTrue(is_clique(self.g4_self, [0, 1, 3]))

        self.assertFalse(is_clique(self.g4_self, [0, 1, 2]))
        self.assertFalse(is_clique(self.g4_self, [0, 2]))
        self.assertFalse(is_clique(self.g4_self, [2, 3]))
        self.assertFalse(is_clique(self.g4_self, [1, 2, 3]))

    def test_is_clique_5(self):
        """Test is_clique on one of the graphs."""
        self.assertTrue(is_clique(self.g5, []))
        self.assertTrue(is_clique(self.g5, [4]))
        self.assertTrue(is_clique(self.g5, [3]))
        self.assertTrue(is_clique(self.g5, [0, 1]))
        self.assertTrue(is_clique(self.g5, [2, 4]))
        self.assertTrue(is_clique(self.g5, [1, 3, 4]))
        self.assertTrue(is_clique(self.g5, [1, 2, 3]))
        self.assertTrue(is_clique(self.g5, [0, 1, 2]))
        self.assertTrue(is_clique(self.g5, [1, 2, 3, 4]))

        self.assertFalse(is_clique(self.g5, [0, 1, 2, 3]))
        self.assertFalse(is_clique(self.g5, [0, 1, 2, 4]))
        self.assertFalse(is_clique(self.g5, [0, 1, 2, 3, 4]))
        self.assertFalse(is_clique(self.g5, [0, 4]))
        self.assertFalse(is_clique(self.g5, [0, 3]))

    def test_is_clique_6(self):
        """Test is_clique on one of the graphs."""
        self.assertTrue(is_clique(self.g6, []))
        self.assertTrue(is_clique(self.g6, [1]))
        self.assertTrue(is_clique(self.g6, [5]))
        self.assertTrue(is_clique(self.g6, [0, 3]))
        self.assertTrue(is_clique(self.g6, [1, 5]))
        self.assertTrue(is_clique(self.g6, [1, 2, 5]))

        self.assertFalse(is_clique(self.g6, [0, 1, 4, 5]))
        self.assertFalse(is_clique(self.g6, [0, 1, 3]))
        self.assertFalse(is_clique(self.g6, [0, 4]))
        self.assertFalse(is_clique(self.g6, [2, 4]))

    def test_clique_expansion_options_4(self):
        """Test clique_expansion_options on one of the graphs."""
        self.assertEqual(clique_expansion_options(self.g4, []), [0, 1, 2, 3])
        self.assertEqual(clique_expansion_options(self.g4, [0]), [1, 3])
        self.assertEqual(clique_expansion_options(self.g4, [1]), [0, 2, 3])
        self.assertEqual(clique_expansion_options(self.g4, [2]), [1])
        self.assertEqual(clique_expansion_options(self.g4, [3]), [0, 1])
        self.assertEqual(clique_expansion_options(self.g4, [1, 2]), [])
        self.assertEqual(clique_expansion_options(self.g4, [0, 1]), [3])
        self.assertEqual(clique_expansion_options(self.g4, [1, 3]), [0])
        self.assertEqual(clique_expansion_options(self.g4, [0, 3]), [1])
        self.assertEqual(clique_expansion_options(self.g4, [0, 1, 3]), [])

    def test_clique_expansion_options_4(self):
        """Test clique_expansion_options on one of the graphs."""
        self.assertEqual(clique_expansion_options(self.g4_self, []), [0, 1, 2, 3])
        self.assertEqual(clique_expansion_options(self.g4_self, [0]), [1, 3])
        self.assertEqual(clique_expansion_options(self.g4_self, [1]), [0, 2, 3])
        self.assertEqual(clique_expansion_options(self.g4_self, [2]), [1])
        self.assertEqual(clique_expansion_options(self.g4_self, [3]), [0, 1])
        self.assertEqual(clique_expansion_options(self.g4_self, [1, 2]), [])
        self.assertEqual(clique_expansion_options(self.g4_self, [0, 1]), [3])
        self.assertEqual(clique_expansion_options(self.g4_self, [1, 3]), [0])
        self.assertEqual(clique_expansion_options(self.g4_self, [0, 3]), [1])
        self.assertEqual(clique_expansion_options(self.g4_self, [0, 1, 3]), [])

    def test_clique_expansion_options_5(self):
        """Test clique_expansion_options on one of the graphs."""
        self.assertEqual(clique_expansion_options(self.g5, []), [0, 1, 2, 3, 4])
        self.assertEqual(clique_expansion_options(self.g5, [0]), [1, 2])
        self.assertEqual(clique_expansion_options(self.g5, [1]), [0, 2, 3, 4])
        self.assertEqual(clique_expansion_options(self.g5, [2]), [0, 1, 3, 4])
        self.assertEqual(clique_expansion_options(self.g5, [3]), [1, 2, 4])
        self.assertEqual(clique_expansion_options(self.g5, [4]), [1, 2, 3])
        self.assertEqual(clique_expansion_options(self.g5, [1, 2]), [0, 3, 4])
        self.assertEqual(clique_expansion_options(self.g5, [1, 2, 4]), [3])
        self.assertEqual(clique_expansion_options(self.g5, [1, 3]), [2, 4])
        self.assertEqual(clique_expansion_options(self.g5, [0, 1]), [2])

    def test_clique_greedy_4(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(clique_greedy(self.g4), [0, 1, 3])

    def test_clique_greedy_4_sub(self):
        """Test greedy search on one of the graphs."""
        g4 = Graph(4, undirected=True)
        g4.insert_edge(0, 1, 1.0)
        g4.insert_edge(0, 2, 1.0)
        g4.insert_edge(0, 3, 1.0)
        g4.insert_edge(2, 3, 1.0)
        self.assertEqual(clique_greedy(g4), [0, 1])

    def test_clique_greedy_5(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(clique_greedy(self.g5), [0, 1, 2])

    def test_clique_greedy_6(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(clique_greedy(self.g6), [0, 1])

    def test_clique_greedy_6b(self):
        """Test greedy search on one of the graphs."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)
        self.assertEqual(clique_greedy(g), [0, 1])

    def test_clique_greedy_8(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(clique_greedy(self.g8), [0, 1])

    def test_maximum_clique_4(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_clique_backtracking(self.g4), [0, 1, 3])

    def test_maximum_clique_4_self(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_clique_backtracking(self.g4_self), [0, 1, 3])

    def test_maximum_clique_4b(self):
        """Test backtracking search on one of the graphs."""
        g4 = Graph(4, undirected=True)
        g4.insert_edge(0, 1, 1.0)
        g4.insert_edge(0, 2, 1.0)
        g4.insert_edge(0, 3, 1.0)
        g4.insert_edge(2, 3, 1.0)
        self.assertEqual(maximum_clique_backtracking(g4), [0, 2, 3])

    def test_maximum_clique_5(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_clique_backtracking(self.g5), [1, 2, 3, 4])

    def test_maximum_clique_6(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_clique_backtracking(self.g6), [1, 2, 5])

    def test_maximum_clique_8(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_clique_backtracking(self.g8), [3, 4, 6, 7])


if __name__ == "__main__":
    unittest.main()
