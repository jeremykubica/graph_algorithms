from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.clustering_coefficient import *

import unittest


class TestGraphMetrics(unittest.TestCase):

    def setUp(self):
        """Create three graphs to be used in the tests."""
        self.g4 = Graph(4, undirected=True)
        self.g4.insert_edge(0, 1, 1.0)
        self.g4.insert_edge(0, 2, 1.0)
        self.g4.insert_edge(1, 2, 1.0)

        self.g6star = Graph(6, undirected=True)
        self.g6star.insert_edge(0, 1, 1.0)
        self.g6star.insert_edge(0, 2, 1.0)
        self.g6star.insert_edge(0, 3, 1.0)
        self.g6star.insert_edge(0, 4, 1.0)
        self.g6star.insert_edge(0, 5, 1.0)
        self.g6star.insert_edge(1, 2, 1.0)
        self.g6star.insert_edge(2, 3, 1.0)
        self.g6star.insert_edge(3, 4, 1.0)
        self.g6star.insert_edge(4, 5, 1.0)
        self.g6star.insert_edge(5, 1, 1.0)

        self.g6 = Graph(6, undirected=True)
        self.g6.insert_edge(0, 1, 1.0)
        self.g6.insert_edge(0, 3, 1.0)
        self.g6.insert_edge(0, 4, 1.0)
        self.g6.insert_edge(1, 2, 1.0)
        self.g6.insert_edge(1, 4, 1.0)
        self.g6.insert_edge(2, 4, 1.0)
        self.g6.insert_edge(2, 5, 1.0)
        self.g6.insert_edge(4, 5, 1.0)

    def test_neighbors(self):
        """Test that we can get a node's out neighbors."""
        self.assertEqual(self.g6.nodes[0].get_out_neighbors(), set([1, 3, 4]))
        self.assertEqual(self.g6.nodes[1].get_out_neighbors(), set([0, 2, 4]))
        self.assertEqual(self.g6.nodes[2].get_out_neighbors(), set([1, 4, 5]))
        self.assertEqual(self.g6.nodes[3].get_out_neighbors(), set([0]))
        self.assertEqual(self.g6.nodes[4].get_out_neighbors(), set([0, 1, 2, 5]))
        self.assertEqual(self.g6.nodes[5].get_out_neighbors(), set([2, 4]))

    def test_clustering_coefficient(self):
        """Test that we can compute the clustering coefficient for a single node."""
        self.assertEqual(clustering_coefficient(self.g4, 0), 1.0)
        self.assertEqual(clustering_coefficient(self.g4, 1), 1.0)
        self.assertEqual(clustering_coefficient(self.g4, 2), 1.0)
        self.assertEqual(clustering_coefficient(self.g4, 3), 0.0)

        self.assertAlmostEqual(clustering_coefficient(self.g6, 0), 1.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6, 1), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6, 2), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6, 3), 0.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6, 4), 0.5)
        self.assertAlmostEqual(clustering_coefficient(self.g6, 5), 1.0)

        self.assertAlmostEqual(clustering_coefficient(self.g6star, 0), 0.5)
        self.assertAlmostEqual(clustering_coefficient(self.g6star, 1), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6star, 2), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6star, 3), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6star, 4), 2.0 / 3.0)
        self.assertAlmostEqual(clustering_coefficient(self.g6star, 5), 2.0 / 3.0)

    def test_ave_clustering_coefficient(self):
        """Test that we can compute the average clustering coefficient for a graph."""
        self.assertAlmostEqual(ave_clustering_coefficient(self.g4), 0.75)
        self.assertAlmostEqual(ave_clustering_coefficient(self.g6), 0.52777777777777)
        self.assertAlmostEqual(ave_clustering_coefficient(self.g6star), 0.6388888888888888)


if __name__ == "__main__":
    unittest.main()
