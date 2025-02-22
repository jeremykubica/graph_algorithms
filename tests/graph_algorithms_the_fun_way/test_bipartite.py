import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.bipartite import *


class TestBipartite(unittest.TestCase):
    def test_is_bipartite_3(self):
        """Test bipartite labeling."""
        g = Graph(3, undirected=True)
        self.assertEqual(bipartite_labeling(g), [True, True, True])

        g.insert_edge(0, 1, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True])

        g.insert_edge(1, 2, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True])

        g.insert_edge(2, 0, 1.0)
        self.assertIsNone(bipartite_labeling(g))

    def test_is_bipartite_4(self):
        """Test bipartite labeling."""
        g = Graph(4, undirected=True)
        self.assertEqual(bipartite_labeling(g), [True, True, True, True])

        g.insert_edge(0, 1, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True, True])

        g.insert_edge(1, 2, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True, True])

        g.insert_edge(0, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True, False])

        g.insert_edge(1, 3, 1.0)
        self.assertIsNone(bipartite_labeling(g))

    def test_is_bipartite_5(self):
        """Test bipartite labeling."""
        g = Graph(5, undirected=True)
        self.assertEqual(bipartite_labeling(g), [True, True, True, True, True])

        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 3, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, True, True, False, False])

        g.insert_edge(1, 2, 1.0)
        g.insert_edge(0, 2, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, True, False, False, False])

        g.insert_edge(2, 4, 1.0)
        self.assertIsNone(bipartite_labeling(g))

    def test_is_bipartite_7(self):
        """Test bipartite labeling from figure 15-4."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(2, 1, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 3, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(6, 1, 1.0)
        self.assertEqual(bipartite_labeling(g), [True, False, True, False, True, False, True])

    def test_is_bipartite_7_fail(self):
        """Test bipartite labeling that fails from Figure 15-5."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 1, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 3, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(6, 1, 1.0)
        self.assertIsNone(bipartite_labeling(g))

    def test_max_flow_matching_4(self):
        """Test maximum flow bipartite matching."""
        g = Graph(4, undirected=True)

        # No edges
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [-1, -1, -1, -1])

        # One edge
        g.insert_edge(0, 1, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [1, 0, -1, -1])

        # Second edge to the same node
        g.insert_edge(2, 1, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [1, 0, -1, -1])

        # Third edge to a different node
        g.insert_edge(2, 3, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [1, 0, 3, 2])

        # Fully connected bipartite
        g.insert_edge(0, 3, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [1, 0, 3, 2])

    def test_max_flow_matching5(self):
        """Test maximum flow bipartite matching."""
        g = Graph(5, undirected=True)

        # No edges
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [-1, -1, -1, -1, -1])

        # Edges out of node zero
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [2, -1, 0, -1, -1])

        # Edge out of node one
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [2, 4, 0, -1, 1])

    def test_max_flow_matching_7(self):
        """Test maximum flow bipartite matching."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(2, 1, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 3, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(6, 1, 1.0)

        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [3, 2, 1, 0, 5, 4, -1])

        g.insert_edge(1, 3, 1.0)
        result = bipartite_matching_max_flow(g)
        self.assertIsNone(result)

    def test_max_flow_matching_9(self):
        """Test maximum flow bipartite matching."""
        g = Graph(9, undirected=True)
        g.insert_edge(0, 1, 1)
        g.insert_edge(0, 5, 1)
        g.insert_edge(0, 7, 1)
        g.insert_edge(2, 1, 1)
        g.insert_edge(4, 3, 1)
        g.insert_edge(4, 7, 1)
        g.insert_edge(6, 1, 1)
        g.insert_edge(8, 3, 1)

        result = bipartite_matching_max_flow(g)
        self.assertEqual(result, [5, 2, 1, 8, 7, 0, -1, 4, 3])

    def test_bipartite_max_weight_matching_exhaustive_4(self):
        """Test exhaustive bipartite matching."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1)
        g.insert_edge(0, 3, 1)
        g.insert_edge(2, 1, 2)
        g.insert_edge(2, 3, 3)
        res = bipartite_matching_exh(g)
        self.assertEqual(res, [1, 0, 3, 2])

        g.insert_edge(0, 3, 3)
        res = bipartite_matching_exh(g)
        self.assertEqual(res, [3, 2, 1, 0])

    def test_bipartite_max_weight_matching_exhaustive_5(self):
        """Test exhaustive bipartite matching."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1)
        g.insert_edge(0, 3, 1)
        g.insert_edge(2, 1, 3)
        g.insert_edge(2, 3, 5)
        g.insert_edge(4, 1, 6)
        g.insert_edge(4, 3, 2)
        res = bipartite_matching_exh(g)
        self.assertEqual(res, [-1, 4, 3, 2, 1])

    def test_bipartite_max_weight_matching_exhaustive_6(self):
        """Test exhaustive bipartite matching."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 3, 5)
        g.insert_edge(0, 5, 1)
        g.insert_edge(2, 1, 3)
        g.insert_edge(2, 3, 2)
        g.insert_edge(2, 5, 1)
        g.insert_edge(4, 1, 3)
        g.insert_edge(4, 3, 2)
        g.insert_edge(4, 5, 4)
        res = bipartite_matching_exh(g)
        self.assertEqual(res, [3, 2, 1, 0, 5, 4])


if __name__ == "__main__":
    unittest.main()
