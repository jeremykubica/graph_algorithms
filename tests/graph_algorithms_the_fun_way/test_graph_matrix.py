from graph_algorithms_the_fun_way.graph_matrix import *

import unittest


class TestGraphMatrix(unittest.TestCase):

    def test_empty(self):
        """Test we can create an empty graph."""
        g = GraphMatrix(0)
        self.assertEqual(0, g.num_nodes)
        self.assertEqual(0, len(g.connections))

    def test_no_edges(self):
        """Test we can create a graph with nodes but no edges."""
        g = GraphMatrix(5)
        self.assertEqual(5, g.num_nodes)
        self.assertEqual(5, len(g.connections))

        for i in range(5):
            for j in range(5):
                self.assertEqual(g.get_edge(i, j), 0.0)

    def test_book_create(self):
        """Test we can create the graph from Chapter 1."""
        g: GraphMatrix = GraphMatrix(5, undirected=False)
        g.set_edge(0, 1, 1.0)
        g.set_edge(0, 3, 1.0)
        g.set_edge(0, 4, 3.0)
        g.set_edge(1, 2, 2.0)
        g.set_edge(1, 4, 1.0)
        g.set_edge(3, 4, 3.0)
        g.set_edge(4, 2, 3.0)
        g.set_edge(4, 3, 3.0)

        # Check that the correct edge are there.
        self.assertEqual(g.get_edge(0, 1), 1.0)
        self.assertEqual(g.get_edge(0, 3), 1.0)
        self.assertEqual(g.get_edge(0, 4), 3.0)
        self.assertEqual(g.get_edge(1, 2), 2.0)
        self.assertEqual(g.get_edge(1, 4), 1.0)
        self.assertEqual(g.get_edge(3, 4), 3.0)
        self.assertEqual(g.get_edge(4, 2), 3.0)
        self.assertEqual(g.get_edge(4, 3), 3.0)

        # Check that non-edges produce zeros.
        self.assertEqual(g.get_edge(0, 2), 0.0)
        self.assertEqual(g.get_edge(1, 0), 0.0)
        self.assertEqual(g.get_edge(1, 3), 0.0)
        self.assertEqual(g.get_edge(2, 4), 0.0)
        self.assertEqual(g.get_edge(3, 0), 0.0)

    def test_insert_undirected_edge(self):
        """Test we can insert undirected edges into a graph."""
        g = GraphMatrix(4, undirected=True)
        g.set_edge(0, 1, 1.0)
        g.set_edge(1, 2, 1.0)
        g.set_edge(2, 3, 1.0)
        g.set_edge(3, 0, 1.0)
        g.set_edge(3, 1, 1.0)

        # Check that the correct edge are there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 0))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 1))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 2))
        self.assertTrue(g.is_edge(0, 3))
        self.assertTrue(g.is_edge(3, 0))
        self.assertTrue(g.is_edge(1, 3))
        self.assertTrue(g.is_edge(3, 1))

        # Check that there are no incorrect edges.
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))

        # Check that errors are raised for invalid indices.
        with self.assertRaises(IndexError):
            g.set_edge(4, 1, 1.0)
        with self.assertRaises(IndexError):
            g.set_edge(3, -1, 1.0)
        with self.assertRaises(IndexError):
            g.set_edge(-1, 1, 2.0)
        with self.assertRaises(IndexError):
            g.set_edge(3, 10, 2.0)

    def test_insert_directed_edge(self):
        """Test we can insert directed edges into a graph."""
        g = GraphMatrix(4)
        g.set_edge(0, 1, 1.0)
        g.set_edge(1, 2, 1.0)
        g.set_edge(2, 3, 1.0)
        g.set_edge(3, 0, 1.0)
        g.set_edge(3, 1, 1.0)

        # Check that the correct edge are there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 0))
        self.assertTrue(g.is_edge(3, 1))

        # Check that there are no incorrect edges.
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))
        self.assertFalse(g.is_edge(1, 0))
        self.assertFalse(g.is_edge(2, 1))
        self.assertFalse(g.is_edge(3, 2))
        self.assertFalse(g.is_edge(0, 3))
        self.assertFalse(g.is_edge(1, 3))

    def test_insert_weighted_edge(self):
        """Test we can insert weighted edges into a graph."""
        g = GraphMatrix(4)
        g.set_edge(0, 1, 0.5)
        g.set_edge(1, 2, 2.0)
        g.set_edge(2, 3, 1.0)
        g.set_edge(3, 0, 1.5)
        g.set_edge(3, 1, -1.0)

        # Check that the correct edge are there.
        self.assertAlmostEqual(g.get_edge(0, 1), 0.5)
        self.assertAlmostEqual(g.get_edge(1, 2), 2.0)
        self.assertAlmostEqual(g.get_edge(2, 3), 1.0)
        self.assertAlmostEqual(g.get_edge(3, 0), 1.5)
        self.assertAlmostEqual(g.get_edge(3, 1), -1.0)

        # Check that there are no incorrect edges.
        self.assertAlmostEqual(g.get_edge(0, 2), 0.0)
        self.assertAlmostEqual(g.get_edge(2, 0), 0.0)
        self.assertAlmostEqual(g.get_edge(1, 0), 0.0)
        self.assertAlmostEqual(g.get_edge(2, 1), 0.0)
        self.assertAlmostEqual(g.get_edge(3, 2), 0.0)
        self.assertAlmostEqual(g.get_edge(0, 3), 0.0)
        self.assertAlmostEqual(g.get_edge(1, 3), 0.0)

    def almostEqualList(self, a, b, delta=1e-5):
        """A helper function for determining if two lists of floats
        are almost equal (similar to numpy's allclose)."""
        self.assertEqual(len(a), len(b))
        for i in range(len(a)):
            self.assertAlmostEqual(a[i], b[i], delta=delta)

    def test_simulate_random_step_2(self):
        """Simulate a random step on a two node graph."""
        g = GraphMatrix(2)
        g.set_edge(0, 0, 0.25)
        g.set_edge(0, 1, 0.75)
        g.set_edge(1, 0, 0.5)
        g.set_edge(1, 1, 0.5)

        self.almostEqualList(g.simulate_random_step([1.0, 0.0]), [0.25, 0.75])
        self.almostEqualList(g.simulate_random_step([0.0, 1.0]), [0.5, 0.5])
        self.almostEqualList(g.simulate_random_step([0.5, 0.5]), [0.375, 0.625])
        self.almostEqualList(g.simulate_random_step([0.1, 0.9]), [0.475, 0.525])

    def test_simulate_random_step_3(self):
        """Simulate a random step on a three node graph."""
        g = GraphMatrix(3)
        g.set_edge(0, 1, 2.0 / 3.0)
        g.set_edge(0, 2, 1.0 / 3.0)
        g.set_edge(1, 0, 0.5)
        g.set_edge(1, 2, 0.5)
        g.set_edge(2, 0, 0.75)
        g.set_edge(2, 1, 0.25)

        self.almostEqualList(g.simulate_random_step([1.0, 0.0, 0.0]), [0.0, 2.0 / 3.0, 1.0 / 3.0])
        self.almostEqualList(g.simulate_random_step([0.0, 1.0, 0.0]), [0.5, 0.0, 0.5])
        self.almostEqualList(g.simulate_random_step([0.0, 0.0, 1.0]), [0.75, 0.25, 0.0])
        self.almostEqualList(g.simulate_random_step([0.5, 0.5, 0.0]), [3.0 / 12.0, 4.0 / 12.0, 5.0 / 12.0])
        self.almostEqualList(g.simulate_random_step([0.1, 0.8, 0.1]), [0.475, 11.0 / 120.0, 13.0 / 30.0])


if __name__ == "__main__":
    unittest.main()
