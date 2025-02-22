import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.independent_sets import *


class TestGraphIndependentSets(unittest.TestCase):

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

    def test_is_independent_set_4(self):
        """Test is_independent_set on one of the graphs."""
        self.assertTrue(is_independent_set(self.g4, []))
        self.assertTrue(is_independent_set(self.g4, [0]))
        self.assertTrue(is_independent_set(self.g4, [1]))
        self.assertTrue(is_independent_set(self.g4, [2, 3]))
        self.assertTrue(is_independent_set(self.g4, [0, 2]))

        self.assertFalse(is_independent_set(self.g4, [0, 1]))
        self.assertFalse(is_independent_set(self.g4, [1, 2]))
        self.assertFalse(is_independent_set(self.g4, [1, 3]))
        self.assertFalse(is_independent_set(self.g4, [0, 3]))
        self.assertFalse(is_independent_set(self.g4, [0, 1, 3]))

    def test_is_independent_set_4b(self):
        """Test is_independent_set on one of the graphs."""
        self.assertTrue(is_independent_set(self.g4b, []))
        self.assertTrue(is_independent_set(self.g4b, [0]))
        self.assertTrue(is_independent_set(self.g4b, [1]))
        self.assertTrue(is_independent_set(self.g4b, [2, 3]))
        self.assertTrue(is_independent_set(self.g4b, [1, 2]))
        self.assertTrue(is_independent_set(self.g4b, [0, 3]))

        self.assertFalse(is_independent_set(self.g4b, [0, 1]))
        self.assertFalse(is_independent_set(self.g4b, [1, 3]))
        self.assertFalse(is_independent_set(self.g4b, [0, 2]))
        self.assertFalse(is_independent_set(self.g4b, [0, 1, 2]))

    def test_is_independent_set_5(self):
        """Test is_independent_set on one of the graphs."""
        self.assertTrue(is_independent_set(self.g5, []))
        self.assertTrue(is_independent_set(self.g5, [4]))
        self.assertTrue(is_independent_set(self.g5, [3]))
        self.assertTrue(is_independent_set(self.g5, [0, 3]))
        self.assertTrue(is_independent_set(self.g5, [0, 4]))

        self.assertFalse(is_independent_set(self.g5, [0, 1, 3]))
        self.assertFalse(is_independent_set(self.g5, [0, 2]))
        self.assertFalse(is_independent_set(self.g5, [1, 2, 4]))

    def test_is_independent_set_6(self):
        """Test is_independent_set on one of the graphs."""
        self.assertTrue(is_independent_set(self.g6, []))
        self.assertTrue(is_independent_set(self.g6, [1]))
        self.assertTrue(is_independent_set(self.g6, [5]))
        self.assertTrue(is_independent_set(self.g6, [0, 4]))
        self.assertTrue(is_independent_set(self.g6, [0, 2, 4]))
        self.assertTrue(is_independent_set(self.g6, [3, 5]))

        self.assertFalse(is_independent_set(self.g6, [0, 1, 4, 5]))
        self.assertFalse(is_independent_set(self.g6, [0, 1, 3]))
        self.assertFalse(is_independent_set(self.g6, [0, 1]))
        self.assertFalse(is_independent_set(self.g6, [0, 3]))
        self.assertFalse(is_independent_set(self.g6, [1, 5]))
        self.assertFalse(is_independent_set(self.g6, [0, 2, 5]))

    def test_independent_set_expansion_options_4(self):
        """Test independent_set_expansion_options on one of the graphs."""
        self.assertEqual(independent_set_expansion_options(self.g4, []), [0, 1, 2, 3])
        self.assertEqual(independent_set_expansion_options(self.g4, [0]), [2])
        self.assertEqual(independent_set_expansion_options(self.g4, [1]), [])
        self.assertEqual(independent_set_expansion_options(self.g4, [2]), [0, 3])
        self.assertEqual(independent_set_expansion_options(self.g4, [3]), [2])

    def test_independent_set_lowest_expansion_4(self):
        """Test independent_set_lowest_expansion on one of the graphs."""
        self.assertEqual(independent_set_lowest_expansion(self.g4, []), 2)
        self.assertEqual(independent_set_lowest_expansion(self.g4, [0]), 2)
        self.assertEqual(independent_set_lowest_expansion(self.g4, [1]), -1)
        self.assertEqual(independent_set_lowest_expansion(self.g4, [2]), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g4, [3]), 2)

    def test_independent_set_expansion_options_5(self):
        """Test independent_set_lowest_expansion on one of the graphs."""
        self.assertEqual(independent_set_lowest_expansion(self.g5, []), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g5, [0]), 3)
        self.assertEqual(independent_set_lowest_expansion(self.g5, [1]), -1)

    def test_independent_set_expansion_options_6(self):
        """Test independent_set_lowest_expansion on one of the graphs."""
        self.assertEqual(independent_set_lowest_expansion(self.g6, []), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [0]), 2)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [1]), 3)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [2]), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [3]), 2)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [4]), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [5]), 0)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [0, 4]), 2)
        self.assertEqual(independent_set_lowest_expansion(self.g6, [0, 2]), 4)

    def test_independent_set_greedy_4(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(independent_set_greedy(self.g4), [2, 0])

    def test_independent_set_greedy_4b(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(independent_set_greedy(self.g4b), [2, 3])

    def test_independent_set_greedy_5(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(independent_set_greedy(self.g5), [0, 3])

    def test_independent_set_greedy_6(self):
        """Test greedy search on one of the graphs."""
        self.assertEqual(independent_set_greedy(self.g6), [0, 2, 4])

    def test_independent_set_greedy_6b(self):
        """Test greedy search on one of the graphs."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 5, 1.0)
        self.assertEqual(independent_set_greedy(g), [0, 1])
        self.assertTrue(is_independent_set(g, [0, 3, 5]))

    def test_independent_set_random_6(self):
        """Test random search on one of the graphs."""
        iset = independent_set_random(self.g6)
        self.assertTrue(is_independent_set(self.g6, iset))

    def test_build_independent_set_random_6(self):
        """Test random search on one of the graphs."""
        iset = build_independent_set_random(self.g6, 10)
        self.assertTrue(is_independent_set(self.g6, iset))

    def test_maximum_independent_set_4(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_independent_set_backtracking(self.g4), [2, 3])

    def test_maximum_independent_set_4b(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_independent_set_backtracking(self.g4b), [2, 3])

    def test_maximum_independent_set_5(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_independent_set_backtracking(self.g5), [0, 4])

    def test_maximum_independent_set_6(self):
        """Test backtracking search on one of the graphs."""
        self.assertEqual(maximum_independent_set_backtracking(self.g6), [0, 2, 4])


if __name__ == "__main__":
    unittest.main()
