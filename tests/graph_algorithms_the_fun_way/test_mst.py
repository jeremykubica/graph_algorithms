from graph_algorithms_the_fun_way.graph import Edge, Graph
from graph_algorithms_the_fun_way.mst import (
    compute_sum_weights,
    kruskals,
    is_spanning_tree,
    prims,
)

import unittest


class TestGraphMST(unittest.TestCase):
    def setUp(self):
        """Set up graphs we will use throughout the tests."""
        self.g3 = Graph(3, undirected=True)
        self.g3.insert_edge(0, 1, 1.0)
        self.g3.insert_edge(0, 2, 2.0)
        self.g3.insert_edge(1, 2, 0.8)

        self.g_dis = Graph(4, undirected=True)
        self.g_dis.insert_edge(0, 1, 1.0)
        self.g_dis.insert_edge(2, 3, 2.0)

        self.g5 = Graph(5, undirected=True)
        self.g5.insert_edge(0, 1, 1.0)
        self.g5.insert_edge(0, 2, 0.5)
        self.g5.insert_edge(2, 3, 0.4)
        self.g5.insert_edge(1, 3, 1.1)
        self.g5.insert_edge(1, 4, 0.2)
        self.g5.insert_edge(3, 4, 1.4)

        self.g5b = Graph(5, undirected=True)
        self.g5b.insert_edge(0, 1, 0.5)
        self.g5b.insert_edge(0, 2, 1.2)
        self.g5b.insert_edge(0, 4, 0.7)
        self.g5b.insert_edge(1, 2, 0.5)
        self.g5b.insert_edge(2, 3, 1.0)
        self.g5b.insert_edge(3, 4, 0.7)

        self.g6 = Graph(6, undirected=True)
        self.g6.insert_edge(0, 1, 1.0)
        self.g6.insert_edge(0, 3, 0.5)
        self.g6.insert_edge(3, 4, 2.0)
        self.g6.insert_edge(1, 4, 0.5)
        self.g6.insert_edge(2, 5, 0.5)
        self.g6.insert_edge(1, 2, 1.0)
        self.g6.insert_edge(1, 5, 0.1)
        self.g6.insert_edge(4, 5, 2.0)

        self.g8 = Graph(8, undirected=True)
        self.g8.insert_edge(0, 1, 1.0)
        self.g8.insert_edge(0, 3, 0.6)
        self.g8.insert_edge(1, 2, 1.2)
        self.g8.insert_edge(1, 4, 0.5)
        self.g8.insert_edge(1, 5, 0.2)
        self.g8.insert_edge(2, 5, 0.4)
        self.g8.insert_edge(3, 4, 1.5)
        self.g8.insert_edge(3, 6, 1.0)
        self.g8.insert_edge(4, 5, 1.5)
        self.g8.insert_edge(5, 6, 2.5)
        self.g8.insert_edge(5, 7, 1.4)
        self.g8.insert_edge(6, 7, 0.3)

    def test_is_spanning_tree(self):
        """Test the is_spanning_tree() function."""
        # Test g3
        edges = []
        self.assertFalse(is_spanning_tree(self.g3, edges))

        edges.append(Edge(0, 1, 1.0))
        edges.append(Edge(2, 0, 2.0))
        self.assertTrue(is_spanning_tree(self.g3, edges))

        # Test g5
        edges = []
        self.assertFalse(is_spanning_tree(self.g5, edges))

        edges.append(Edge(0, 2, 1.0))
        edges.append(Edge(2, 3, 0.4))
        self.assertFalse(is_spanning_tree(self.g5, edges))

        edges.append(Edge(0, 1, 0.1))
        self.assertFalse(is_spanning_tree(self.g5, edges))

        edges.append(Edge(1, 4, 0.2))
        self.assertTrue(is_spanning_tree(self.g5, edges))

        # The set of edges is no longer a tree
        edges.append(Edge(1, 3, 0.1))
        self.assertFalse(is_spanning_tree(self.g5, edges))

    def test_compute_sum_weights(self):
        """Test the compute_sum_weights() function."""
        edges = []
        self.assertAlmostEqual(compute_sum_weights(edges), 0.0)

        edges.append(Edge(0, 2, 1.0))
        edges.append(Edge(2, 3, 0.4))
        self.assertAlmostEqual(compute_sum_weights(edges), 1.4)

        edges.append(Edge(0, 1, 0.1))
        edges.append(Edge(1, 4, 0.2))
        self.assertAlmostEqual(compute_sum_weights(edges), 1.7)

    def test_prims(self):
        """Test Prim's Algorithm."""
        mst3 = prims(self.g3)
        self.assertTrue(is_spanning_tree(self.g3, mst3))
        self.assertAlmostEqual(compute_sum_weights(mst3), 1.8)

        mst5 = prims(self.g5)
        self.assertTrue(is_spanning_tree(self.g5, mst5))
        self.assertAlmostEqual(compute_sum_weights(mst5), 2.1)

        mst5b = prims(self.g5b)
        self.assertTrue(is_spanning_tree(self.g5b, mst5b))
        self.assertAlmostEqual(compute_sum_weights(mst5b), 2.4)

        mst6 = prims(self.g6)
        self.assertTrue(is_spanning_tree(self.g6, mst6))
        self.assertAlmostEqual(compute_sum_weights(mst6), 2.6)

        mst8 = prims(self.g8)
        self.assertTrue(is_spanning_tree(self.g8, mst8))
        self.assertAlmostEqual(compute_sum_weights(mst8), 4.0)

        mst_dis = prims(self.g_dis)
        self.assertIsNone(mst_dis)
        self.assertFalse(is_spanning_tree(self.g_dis, mst_dis))

    def test_kruskals(self):
        """Test Kruskal's algorithm."""
        mst3 = kruskals(self.g3)
        self.assertTrue(is_spanning_tree(self.g3, mst3))
        self.assertAlmostEqual(compute_sum_weights(mst3), 1.8)

        mst5 = kruskals(self.g5)
        self.assertTrue(is_spanning_tree(self.g5, mst5))
        self.assertAlmostEqual(compute_sum_weights(mst5), 2.1)

        mst5b = kruskals(self.g5b)
        self.assertTrue(is_spanning_tree(self.g5b, mst5b))
        self.assertAlmostEqual(compute_sum_weights(mst5b), 2.4)

        mst6 = kruskals(self.g6)
        self.assertTrue(is_spanning_tree(self.g6, mst6))
        self.assertAlmostEqual(compute_sum_weights(mst6), 2.6)

        mst8 = kruskals(self.g8)
        self.assertTrue(is_spanning_tree(self.g8, mst8))
        self.assertAlmostEqual(compute_sum_weights(mst8), 4.0)

        mst_dis = kruskals(self.g_dis)
        self.assertIsNone(mst_dis)
        self.assertFalse(is_spanning_tree(self.g_dis, mst_dis))


if __name__ == "__main__":
    unittest.main()
