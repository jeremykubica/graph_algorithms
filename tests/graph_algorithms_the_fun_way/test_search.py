import math
import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.paths import last_path_length
from graph_algorithms_the_fun_way.search import (
    astar_search,
    breadth_first_search,
    depth_first_search_basic,
    depth_first_search_basic_all,
    depth_first_search_path,
    depth_first_search_stack,
    dfs_connected_components,
    dfs_preorder,
    greedy_search,
)


def euclidean_dist(x1: float, y1: float, x2: float, y2: float) -> float:
    """A Euclidean distance function for heuristic computation.

    Parameters
    ----------
    x1 : float
        The x value of the first point.
    y1 : float
        The y value of the first point.
    x2 : float
        The x value of the second point.
    y2 : float
        The y value of the second point.

    Returns
    -------
    dist : float
        The Euclidean distance between the two points.
    """
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class TestSearch(unittest.TestCase):
    def test_simple_bfs(self):
        """Test BFS on a graph with 3 nodes."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        path = breadth_first_search(g, 0)
        self.assertEqual(path, [-1, 0, 0])

    def test_bfs9(self):
        """Test BFS on a graph with 9 nodes."""
        g = Graph(9, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(0, 7, 1.0)

        path = breadth_first_search(g, 0)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 0, 5, 0, 5])

    def test_bfs10(self):
        """Test BFS on a graph with 10 nodes."""
        g = Graph(10, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 7, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 9, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(7, 8, 1.0)
        g.insert_edge(8, 9, 1.0)

        path = breadth_first_search(g, 0)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 0, 5, 0, 5, 8])

        # Test step sizes from Figure 5-2.
        self.assertEqual(last_path_length(path, 0, goal=0), 0)
        self.assertEqual(last_path_length(path, 1, goal=0), 1)
        self.assertEqual(last_path_length(path, 2, goal=0), 2)
        self.assertEqual(last_path_length(path, 3, goal=0), 3)
        self.assertEqual(last_path_length(path, 4, goal=0), 3)
        self.assertEqual(last_path_length(path, 5, goal=0), 1)
        self.assertEqual(last_path_length(path, 6, goal=0), 2)
        self.assertEqual(last_path_length(path, 7, goal=0), 1)
        self.assertEqual(last_path_length(path, 8, goal=0), 2)
        self.assertEqual(last_path_length(path, 9, goal=0), 3)

    def test_bfs_figure5_3(self):
        """Test BFS on a graph from Figure 5-3."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 10.0)
        g.insert_edge(1, 2, 1.0)

        path = breadth_first_search(g, 0)
        self.assertEqual(path, [-1, 0, 0])

        # Test step sizes from Figure 5-3.
        self.assertEqual(last_path_length(path, 0, goal=0), 0)
        self.assertEqual(last_path_length(path, 1, goal=0), 1)
        self.assertEqual(last_path_length(path, 2, goal=0), 1)

    def test_simple_dfs3(self):
        """Test DFS on a graph with 3 nodes."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, 1])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_simple_dfs4(self):
        """Test DFS on a graph with 4 nodes."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(0, 3, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, 1, 0])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_dfs9(self):
        """Test DFS on a graph with 9 nodes."""
        g = Graph(9, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(0, 7, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 0, 5, 0, 6])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_dfs10(self):
        """Test DFS on a graph with 10 nodes."""
        g = Graph(10, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 7, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 9, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(7, 8, 1.0)
        g.insert_edge(8, 9, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 8, 5, 8, 9, 4])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_dfs_disconnected(self):
        """Test DFS on a disconnected graph."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, -1, -1])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_dfs_disconnected2(self):
        """Test DFS on a second disconnected graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(3, 4, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, -1, -1, 3])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_dfs_disconnected3(self):
        """Test DFS on a third disconnected graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(4, 3, 1.0)

        path = depth_first_search_path(g)
        self.assertEqual(path, [-1, 0, -1, -1, -1])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_depth_first_search_stack3(self):
        """Test DFS with a stack on a graph with 3 nodes."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        path = depth_first_search_stack(g, 0)
        self.assertEqual(path, [-1, 0, 1])

        depth_first_search_basic(g, 0)
        depth_first_search_basic_all(g)

    def test_depth_first_search_stack9(self):
        """Test DFS with a stack on a graph with 9 nodes."""
        g = Graph(9, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(0, 7, 1.0)

        path = depth_first_search_stack(g, 0)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 0, 5, 0, 6])

    def test_depth_first_search_stack10(self):
        """Test DFS with a stack on a graph with 10 nodes."""
        g = Graph(10, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 7, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 9, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(5, 8, 1.0)
        g.insert_edge(6, 8, 1.0)
        g.insert_edge(7, 8, 1.0)
        g.insert_edge(8, 9, 1.0)

        path = depth_first_search_stack(g, 0)
        self.assertEqual(path, [-1, 0, 1, 2, 2, 8, 5, 8, 9, 4])

    def test_greedy_simple(self):
        """Test greedy search on a simple graph with 4 nodes."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 0.5)

        h = [2.0, 1.0, 0.5, 0.0]
        last = greedy_search(g, h, 0, 3)
        self.assertEqual(last, [-1, 0, 0, 2])

    def test_greedy_complex(self):
        """Test greedy search on a more complex graph."""
        g: Graph = Graph(7, undirected=True)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 2.83)
        g.insert_edge(0, 3, 3.0)
        g.insert_edge(1, 4, 1.41)
        g.insert_edge(2, 3, 2.24)
        g.insert_edge(2, 4, 3.5)
        g.insert_edge(3, 5, 1.14)
        g.insert_edge(4, 6, 2.24)
        g.insert_edge(5, 6, 3.16)
        h: list = [5.0, 3.6, 2.24, 4.0, 2.24, 3.16, 0.0]
        last: list = greedy_search(g, h, 0, 6)
        self.assertEqual(last, [-1, 0, 0, 0, 2, 6, 4])

    def test_astar_simple(self):
        """Test A* search on a simple graph with 4 nodes."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 0.5)

        h = [2.0, 1.0, 0.5, 0.0]
        last = astar_search(g, h, 0, 3)
        self.assertEqual(last, [-1, 0, 0, 2])

    def test_heuristic_example_settings(self):
        """Test that the heuristic values we set match those given in the Figures."""
        # Heuristic values of the nodes
        self.assertAlmostEqual(euclidean_dist(0, 0, 3, 4), 5.0, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(0, 2, 3, 4), 3.6, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(2, 2, 3, 4), 2.24, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(3, 0, 3, 4), 4.0, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(1, 3, 3, 4), 2.24, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(4, 1, 3, 4), 3.16, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(3, 4, 3, 4), 0.0, delta=0.05)

        # Edge weights
        self.assertAlmostEqual(euclidean_dist(0, 0, 0, 2), 2.0, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(0, 0, 2, 2), 2.83, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(0, 0, 3, 0), 3.0, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(0, 2, 1, 3), 1.41, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(2, 2, 1, 3), 1.41, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(2, 2, 3, 0), 2.24, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(3, 0, 4, 1), 1.41, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(1, 3, 3, 4), 2.24, delta=0.05)
        self.assertAlmostEqual(euclidean_dist(4, 1, 3, 4), 3.16, delta=0.05)

    def test_astar_complex(self):
        """Test A* search on a more complex graph."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 2.83)
        g.insert_edge(0, 3, 3.0)
        g.insert_edge(1, 4, 1.41)
        g.insert_edge(2, 3, 2.24)
        g.insert_edge(3, 5, 1.14)
        g.insert_edge(4, 6, 2.24)
        g.insert_edge(5, 6, 3.16)
        g.insert_edge(2, 4, 3.5)

        h = [5.0, 3.6, 2.24, 4.0, 2.24, 3.16, 0.0]
        last: list = astar_search(g, h, 0, 6)
        self.assertEqual(last, [-1, 0, 0, 0, 1, 6, 4])

    def test_dfs_connected_components_4(self):
        """Test DFS connected component search on a graph with 4 nodes."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 2])

        g.insert_edge(0, 2, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 0, 1])

        g.insert_edge(1, 2, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 0, 1])

        g.insert_edge(2, 3, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 0, 0])

    def test_dfs_connected_components_5(self):
        """Test DFS connected component search on a graph with 5 nodes."""
        g = Graph(5, undirected=True)
        g.insert_edge(2, 3, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 2, 2, 3])

        g.insert_edge(3, 4, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 2, 2, 2])

        g.insert_edge(4, 2, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 2, 2, 2])

        g.insert_edge(0, 4, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 0, 0, 0])

        g.insert_edge(0, 3, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 0, 0, 0])

        g.insert_edge(0, 2, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 1, 0, 0, 0])

    def test_dfs_connected_components_6(self):
        """Test DFS connected component search on a graph with 6 nodes."""
        g = Graph(6, undirected=True)
        self.assertEqual(dfs_connected_components(g), [0, 1, 2, 3, 4, 5])

        g.insert_edge(0, 1, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 2, 3, 4])

        g.insert_edge(1, 1, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 2, 3, 4])

        g.insert_edge(4, 5, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 2, 3, 3])

        g.insert_edge(0, 3, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 0, 2, 2])

        g.insert_edge(3, 3, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 0, 2, 2])

        g.insert_edge(2, 5, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 0, 1, 1])

        g.insert_edge(2, 4, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 1, 0, 1, 1])

    def test_def_connected_components_8(self):
        """Test DFS connected component search on a graph with 8 nodes."""
        g = Graph(8, undirected=True)
        self.assertEqual(dfs_connected_components(g), [0, 1, 2, 3, 4, 5, 6, 7])

        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 7, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 0, 1, 0, 2, 2, 1])

        g.insert_edge(2, 6, 1.0)
        self.assertEqual(dfs_connected_components(g), [0, 0, 0, 1, 0, 0, 0, 1])

    def test_figure_11_7(self):
        """Test the preorder list in Figure 11-7."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 6, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 5, 1.0)
        order, parents = dfs_preorder(g)
        self.assertEqual(order, [0, 1, 2, 5, 3, 6, 4])
        self.assertEqual(parents, [-1, 0, 1, 0, 2, 3, 1])

    def test_figure_11_8(self):
        """Test the preorder list in Figure 11-8."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 6, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 5, 1.0)
        order, parents = dfs_preorder(g)
        self.assertEqual(order, [0, 1, 2, 5, 3, 6, 4])
        self.assertEqual(parents, [-1, 0, 1, 0, 2, 3, 1])

    def test_figure_11_10(self):
        """Test the preorder list in Figure 11-10."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 6, 1.0)
        g.insert_edge(3, 7, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(6, 7, 1.0)
        order, parents = dfs_preorder(g)
        self.assertEqual(order, [0, 1, 2, 3, 6, 7, 5, 4])
        self.assertEqual(parents, [-1, 0, 1, 2, 1, 4, 7, 3])

    def test_figure_11_11(self):
        """Test the preorder list in Figure 11-11."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 6, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 5, 1.0)
        order, parents = dfs_preorder(g)
        self.assertEqual(order, [0, 1, 2, 5, 3, 6, 4])
        self.assertEqual(parents, [-1, 0, 1, 0, 2, 3, 1])


if __name__ == "__main__":
    unittest.main()
