import random
import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.random_walks import *


def _build_node_occurrence_hist(num_nodes: int, walk: list) -> list:
    """Construct a histogram of how often each node was visited.

    Parameters
    ----------
    num_nodes : int
        The total number of nodes
    walk : list
        The nodes visited on the walk.

    Returns
    -------
    hist : list
        For each node the count of times it was visited.
    """
    hist: list = [0] * num_nodes
    for n in walk:
        hist[n] += 1
    return hist


class TestMarkovGraph(unittest.TestCase):
    def _next_step_hist(self, g: Graph, index: int, steps: int) -> list:
        """Create a histogram of the number of times we moved from
        the given node to each other node.

        Parameters
        ----------
        g : Graph
            The input graph.
        index : int
            The index of the query node.
        steps : int
            The number of samples.

        Returns
        -------
        hist : list
            For each node the count of times it was visited.
        """
        node: Node = g.nodes[index]
        samples: list = [-1] * steps
        for i in range(steps):
            samples[i] = choose_next_node(node)
        return _build_node_occurrence_hist(g.num_nodes, samples)

    def setUp(self):
        """Create a known graph and set a seed to control randomness."""
        random.seed(10)

        self.g4 = Graph(4)
        self.g4.insert_edge(0, 1, 0.5)
        self.g4.insert_edge(0, 2, 0.5)
        self.g4.insert_edge(1, 0, 0.1)
        self.g4.insert_edge(1, 2, 0.3)
        self.g4.insert_edge(1, 3, 0.6)
        self.g4.insert_edge(2, 0, 0.2)
        self.g4.insert_edge(2, 3, 0.8)
        self.g4.insert_edge(3, 1, 0.2)
        self.g4.insert_edge(3, 2, 0.6)
        self.g4.insert_edge(3, 3, 0.2)

    def test_is_valid_probability_graph_3(self):
        """Test is_valid_probability_graph."""
        g = Graph(3)
        self.assertFalse(is_valid_probability_graph(g))

        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        self.assertTrue(is_valid_probability_graph(g))

        g.insert_edge(0, 1, 0.25)
        g.insert_edge(0, 2, 0.75)
        self.assertTrue(is_valid_probability_graph(g))

        g.insert_edge(1, 1, 0.4)
        g.insert_edge(1, 2, 0.6)
        self.assertTrue(is_valid_probability_graph(g))

        # Prob leaving node 0 too small.
        g.insert_edge(1, 1, 0.1)
        self.assertFalse(is_valid_probability_graph(g))

        # Prob leaving node 0 too large.
        g.insert_edge(1, 1, 0.5)
        self.assertFalse(is_valid_probability_graph(g))

    def test_is_valid_probability_graph_4(self):
        """Test is_valid_probability_graph."""
        self.assertTrue(is_valid_probability_graph(self.g4))

        self.g4.insert_edge(2, 2, 0.1)
        self.assertFalse(is_valid_probability_graph(self.g4))

    def test_choose_next_node(self):
        """Check we can sample fthe next node."""
        hist0 = self._next_step_hist(self.g4, 0, 1000)
        self.assertEqual(hist0[0], 0)
        self.assertTrue(450 < hist0[1] < 550)
        self.assertTrue(450 < hist0[2] < 550)
        self.assertEqual(hist0[3], 0)

        hist1 = self._next_step_hist(self.g4, 1, 1000)
        self.assertTrue(50 < hist1[0] < 150)
        self.assertEqual(hist1[1], 0)
        self.assertTrue(250 < hist1[2] < 350)
        self.assertTrue(550 < hist1[3] < 650)

        hist2 = self._next_step_hist(self.g4, 2, 1000)
        self.assertTrue(150 < hist2[0] < 250)
        self.assertEqual(hist2[1], 0)
        self.assertEqual(hist2[2], 0)
        self.assertTrue(750 < hist2[3] < 850)

        hist3 = self._next_step_hist(self.g4, 3, 1000)
        self.assertEqual(hist3[0], 0)
        self.assertTrue(150 < hist3[1] < 250)
        self.assertTrue(550 < hist3[2] < 650)
        self.assertTrue(150 < hist3[3] < 250)

    def test_random_walk(self):
        """Test that we can generate a random walk."""
        num_steps = 1000
        walk = random_walk(self.g4, 0, 1000)
        self.assertEqual(len(walk), num_steps)

        hist = _build_node_occurrence_hist(self.g4.num_nodes, walk)
        self.assertGreater(hist[0], 0)
        self.assertGreater(hist[1], 0)
        self.assertGreater(hist[2], 0)
        self.assertGreater(hist[3], 0)
        self.assertGreater(hist[3], hist[0])
        self.assertGreater(hist[3], hist[1])
        self.assertLess(hist[0], num_steps)
        self.assertLess(hist[1], num_steps)
        self.assertLess(hist[2], num_steps)
        self.assertLess(hist[3], num_steps)

    def test_random_walk_3(self):
        """Test that we can generate a random walk."""
        g = Graph(3)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        # Deterministic cycle
        walk = random_walk(g, 0, 99)
        hist = _build_node_occurrence_hist(3, walk)
        self.assertEqual(hist[0], 33)
        self.assertEqual(hist[1], 33)
        self.assertEqual(hist[2], 33)

        # Equal prob from zero.
        g2 = Graph(3)
        g2.insert_edge(0, 1, 0.5)
        g2.insert_edge(0, 2, 0.5)
        g2.insert_edge(1, 0, 1.0)
        g2.insert_edge(2, 0, 1.0)

        walk = random_walk(g2, 0, 10)
        hist = _build_node_occurrence_hist(3, walk)
        self.assertEqual(hist[0], 5)

        # Test invalid graph
        g.insert_edge(2, 0, 0.8)
        with self.assertRaises(ValueError):
            walk_invalid = random_walk(g, 0, 1000)

    def test_random_walk_disconnected(self):
        """Test that we can generate a random walk."""
        g = Graph(3)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(2, 2, 1.0)

        # Deterministic cycle
        walk = random_walk(g, 0, 100)
        hist = _build_node_occurrence_hist(3, walk)
        self.assertEqual(hist[0], 50)
        self.assertEqual(hist[1], 50)
        self.assertEqual(hist[2], 0)

    def test_random_start(self):
        """Test that we can sample a starting node."""
        S = [0.1, 0.4, 0.25, 0.1, 0.15]
        hist = [0.0, 0.0, 0.0, 0.0, 0.0]
        num_samples = 1000
        for i in range(num_samples):
            hist[choose_start(S)] += 1.0

        for j in range(len(S)):
            self.assertAlmostEqual(S[j], hist[j] / num_samples, delta=0.05)

    def test_random_startB(self):
        """Test that we can sample a starting node."""
        S = [0.3, 0.2, 0.25, 0.25]
        hist = [0.0, 0.0, 0.0, 0.0]
        num_samples = 1000
        for i in range(num_samples):
            hist[choose_start(S)] += 1.0

        for j in range(len(S)):
            self.assertAlmostEqual(S[j], hist[j] / num_samples, delta=0.05)

    def test_learn_from_walk(self):
        """Test that we can learn a graph from the random walk."""
        path1 = [0, 1, 0, 0, 1, 0, 0]
        path2 = [0, 1, 0, 1, 0, 0, 0]
        g = estimate_graph_from_random_walks([path1, path2])
        self.assertEqual(g.num_nodes, 2)
        self.assertEqual(g.get_edge(0, 0).weight, 0.5)
        self.assertEqual(g.get_edge(0, 1).weight, 0.5)
        self.assertEqual(g.get_edge(1, 0).weight, 1.0)
        self.assertIsNone(g.get_edge(1, 1))

        s = estimate_start_from_random_walks([path1, path2])
        self.assertEqual(len(s), 2)
        self.assertEqual(s[0], 1.0)
        self.assertEqual(s[1], 0.0)

        # Add walks with others starts
        s = estimate_start_from_random_walks([path1, path2, [0], [1]])
        self.assertEqual(len(s), 2)
        self.assertEqual(s[0], 0.75)
        self.assertEqual(s[1], 0.25)

        # Modify path 2 to end on node 1.
        path2 = [0, 1, 0, 1, 0, 0, 0, 0, 1]
        g = estimate_graph_from_random_walks([path1, path2])
        self.assertEqual(g.num_nodes, 2)
        self.assertEqual(g.get_edge(0, 0).weight, 0.5)
        self.assertEqual(g.get_edge(0, 1).weight, 0.5)
        self.assertEqual(g.get_edge(1, 0).weight, 1.0)
        self.assertIsNone(g.get_edge(1, 1))

        # Modify path 2 to start from node 1.
        path2 = [1, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        g = estimate_graph_from_random_walks([path1, path2])
        self.assertEqual(g.num_nodes, 2)
        self.assertEqual(g.get_edge(0, 0).weight, 0.5)
        self.assertEqual(g.get_edge(0, 1).weight, 0.5)
        self.assertEqual(g.get_edge(1, 0).weight, 1.0)
        self.assertIsNone(g.get_edge(1, 1))

        # Test on a variety of data
        paths = [
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0],
            [0, 0, 1],
            [0, 0, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]
        for i in range(len(paths)):
            current_paths = []
            for j in range(i + 1):
                current_paths.append(paths[j])

            g = estimate_graph_from_random_walks(current_paths)
            self.assertEqual(g.num_nodes, 2)
            self.assertEqual(g.get_edge(0, 0).weight, 0.5)
            self.assertEqual(g.get_edge(0, 1).weight, 0.5)
            self.assertEqual(g.get_edge(1, 0).weight, 1.0)
            self.assertIsNone(g.get_edge(1, 1))

    def test_learn_from_walk_2(self):
        """Test that we can learn a graph from the random walk."""
        paths = [
            [0, 1, 3, 2, 3, 3, 2, 0, 2, 3, 2, 3, 3, 1, 3, 2, 3, 2, 3, 2, 3, 2, 0, 2, 3],
            [3, 2, 0, 1, 2, 3, 2, 3, 3, 2, 3, 2, 0, 2, 3, 1, 2, 3, 1, 3, 3, 2, 3, 3, 1],
            [2, 3, 1, 3, 2, 3, 3, 1, 2, 3, 2, 3, 1, 3, 3, 2, 3, 2, 3, 1, 2, 3, 2, 3, 2],
            [0, 1, 2, 0, 1, 3, 2, 3, 2, 3, 2, 3, 2, 3, 1, 3, 2, 3, 2, 3, 2, 3, 1, 3, 3],
            [3, 3, 3, 2, 0, 1, 2, 3, 3, 2, 0, 2, 3, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 0, 1],
            [3, 1, 2, 3, 3, 2, 3, 1, 3, 2, 3, 1, 3, 1, 3, 2, 3, 2, 3, 1, 3, 2, 3, 2, 3],
            [3, 3, 2, 3, 2, 3, 2, 3, 2, 0, 2, 0, 1, 3, 2, 3, 1, 3, 2, 3, 2, 3, 2, 0, 2],
            [3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 3, 3, 2, 0, 2, 3, 1, 2],
            [2, 0, 1, 2, 3, 2, 3, 2, 3, 1, 3, 1, 3, 2, 3, 3, 3, 2, 3, 2, 3, 1, 3, 2, 3],
            [2, 3, 2, 3, 1, 2, 3, 2, 3, 2, 0, 2, 3, 1, 3, 2, 3, 1, 3, 3, 1, 3, 2, 3, 2],
            [3, 3, 1, 3, 3, 2, 3, 2, 0, 1, 2, 3, 1, 3, 2, 3, 2, 3, 2, 0, 1, 2, 3, 1, 2],
            [2, 3, 2, 3, 2, 3, 1, 3, 2, 0, 2, 3, 3, 2, 0, 2, 0, 2, 0, 2, 3, 3, 2, 3, 2],
            [3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 0, 1, 3, 2, 0, 2, 3, 2, 3, 2, 3, 3, 1, 3],
            [0, 1, 3, 1, 3, 2, 3, 2, 3, 2, 3, 1, 2, 3, 3, 2, 3, 2, 3, 2, 3, 1, 0, 1, 0],
            [1, 2, 3, 1, 3, 2, 3, 3, 2, 0, 1, 3, 2, 0, 2, 3, 2, 3, 1, 2, 0, 1, 2, 0, 2],
            [1, 3, 2, 3, 2, 3, 1, 2, 3, 2, 3, 1, 0, 1, 0, 1, 0, 1, 3, 3, 1, 0, 2, 3, 2],
            [3, 3, 1, 3, 1, 3, 2, 3, 3, 2, 3, 2, 0, 1, 2, 3, 2, 3, 2, 3, 2, 3, 2, 0, 2],
            [2, 3, 2, 0, 1, 2, 3, 1, 3, 3, 1, 3, 1, 0, 1, 2, 3, 2, 3, 2, 3, 1, 3, 3, 2],
            [1, 3, 2, 3, 2, 0, 2, 3, 1, 2, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 0, 2, 3, 3],
            [1, 3, 2, 3, 2, 3, 2, 3, 2, 0, 1, 2, 3, 2, 3, 2, 3, 2, 3, 1, 3, 3, 2, 3, 1],
        ]

        g = estimate_graph_from_random_walks(paths)
        self.assertEqual(g.num_nodes, 4)

        self.assertIsNone(g.get_edge(0, 0))
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 0.5, delta=0.05)
        self.assertAlmostEqual(g.get_edge(0, 2).weight, 0.5, delta=0.05)
        self.assertIsNone(g.get_edge(0, 3))

        self.assertAlmostEqual(g.get_edge(1, 0).weight, 0.1, delta=0.05)
        self.assertIsNone(g.get_edge(1, 1))
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 0.3, delta=0.05)
        self.assertAlmostEqual(g.get_edge(1, 3).weight, 0.6, delta=0.05)

        self.assertAlmostEqual(g.get_edge(2, 0).weight, 0.2, delta=0.05)
        self.assertIsNone(g.get_edge(2, 1))
        self.assertIsNone(g.get_edge(2, 2))
        self.assertAlmostEqual(g.get_edge(2, 3).weight, 0.8, delta=0.05)

        self.assertIsNone(g.get_edge(3, 0))
        self.assertAlmostEqual(g.get_edge(3, 1).weight, 0.2, delta=0.05)
        self.assertAlmostEqual(g.get_edge(3, 2).weight, 0.6, delta=0.05)
        self.assertAlmostEqual(g.get_edge(3, 3).weight, 0.2, delta=0.05)

        s = estimate_start_from_random_walks(paths)
        self.assertAlmostEqual(s[0], 3.0 / 20.0)
        self.assertAlmostEqual(s[1], 4.0 / 20.0)
        self.assertAlmostEqual(s[2], 5.0 / 20.0)
        self.assertAlmostEqual(s[3], 8.0 / 20.0)

    def test_learn_from_walk_3(self):
        """Test that we can learn a graph from the random walk."""
        paths = [
            [0, 1, 3],
            [1, 0, 2, 1],
            [1, 0, 2, 1],
            [0, 1, 3, 1, 2],
            [0, 4, 0, 1],
            [0, 2, 1, 3, 0],
            [1, 2, 1, 3, 0],
            [1, 2, 1, 3, 0],
        ]

        g = estimate_graph_from_random_walks(paths)
        self.assertEqual(g.num_nodes, 5)
        self.assertIsNone(g.get_edge(0, 0))
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 3.0 / 7.0)
        self.assertAlmostEqual(g.get_edge(0, 2).weight, 3.0 / 7.0)
        self.assertIsNone(g.get_edge(0, 3))
        self.assertAlmostEqual(g.get_edge(0, 4).weight, 1.0 / 7.0)

        self.assertAlmostEqual(g.get_edge(1, 0).weight, 0.2)
        self.assertIsNone(g.get_edge(1, 1))
        self.assertEqual(g.get_edge(1, 2).weight, 0.3)
        self.assertEqual(g.get_edge(1, 3).weight, 0.5)
        self.assertIsNone(g.get_edge(1, 4))

        self.assertIsNone(g.get_edge(2, 0))
        self.assertEqual(g.get_edge(2, 1).weight, 1.0)
        self.assertIsNone(g.get_edge(2, 2))
        self.assertIsNone(g.get_edge(2, 3))
        self.assertIsNone(g.get_edge(2, 4))

        self.assertEqual(g.get_edge(3, 0).weight, 0.75)
        self.assertEqual(g.get_edge(3, 1).weight, 0.25)
        self.assertIsNone(g.get_edge(3, 2))
        self.assertIsNone(g.get_edge(3, 3))
        self.assertIsNone(g.get_edge(3, 4))

        self.assertEqual(g.get_edge(4, 0).weight, 1.0)
        self.assertIsNone(g.get_edge(4, 1))
        self.assertIsNone(g.get_edge(4, 2))
        self.assertIsNone(g.get_edge(4, 3))
        self.assertIsNone(g.get_edge(4, 4))

        s = estimate_start_from_random_walks(paths)
        self.assertAlmostEqual(s[0], 0.5)
        self.assertAlmostEqual(s[1], 0.5)
        self.assertAlmostEqual(s[2], 0.0)
        self.assertAlmostEqual(s[3], 0.0)


if __name__ == "__main__":
    unittest.main()
