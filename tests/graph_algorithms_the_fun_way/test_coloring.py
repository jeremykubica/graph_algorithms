import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.coloring import *


class TestGraphColoring(unittest.TestCase):
    def test_is_coloring_valid(self):
        """Test is_graph_coloring_valid."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        g.nodes[0].label = 1
        g.nodes[1].label = 2
        self.assertFalse(is_graph_coloring_valid(g))

        g.nodes[2].label = 3
        self.assertTrue(is_graph_coloring_valid(g))

        g.nodes[0].label = 3
        self.assertFalse(is_graph_coloring_valid(g))

    def test_is_coloring_valid2(self):
        """Test is_graph_coloring_valid."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))

        g.nodes[0].label = 1
        g.nodes[1].label = 2
        g.nodes[2].label = 1
        g.nodes[3].label = 3
        self.assertTrue(is_graph_coloring_valid(g))

        g.nodes[3].label = 2
        self.assertTrue(is_graph_coloring_valid(g))

        g.insert_edge(3, 1, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))

    def test_graph_color_greedy_3(self):
        """Test greedy graph coloring."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_graph_color_greedy_4(self):
        """Test greedy graph coloring."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_graph_color_greedy_5(self):
        """Test greedy graph coloring on Figure 16-9."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_graph_color_greedy_5b(self):
        """Test greedy graph coloring on Figure 16-10."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_graph_color_greedy_6(self):
        """Test greedy graph coloring."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_graph_color_greedy_8(self):
        """Test greedy graph coloring."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 6, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))

        graph_color_greedy(g)
        self.assertTrue(is_graph_coloring_valid(g))

    def test_brute_force_3(self):
        """Test brute-force graph coloring."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        self.assertFalse(graph_color_brute_force(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_brute_force(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_brute_force(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_brute_force_4(self):
        """Test brute-force graph coloring."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(1, 3, 1.0)

        self.assertFalse(graph_color_brute_force(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_brute_force(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_brute_force(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_brute_force_5(self):
        """Test brute-force graph coloring."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        self.assertFalse(graph_color_brute_force(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_brute_force(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_brute_force(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_brute_force_6(self):
        """Test brute-force graph coloring."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)

        self.assertFalse(graph_color_brute_force(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_brute_force(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_brute_force(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_brute_force_8(self):
        """Test brute-force graph coloring."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 6, 1.0)

        self.assertFalse(graph_color_brute_force(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_brute_force(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_brute_force(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_3(self):
        """Test DFS graph coloring."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        self.assertFalse(graph_color_dfs(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_4(self):
        """Test DFS graph coloring."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(1, 3, 1.0)

        self.assertFalse(graph_color_dfs(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_5(self):
        """Test DFS graph coloring."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        self.assertFalse(graph_color_dfs(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs(g, 3, 0))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_6(self):
        """Test DFS graph coloring."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)

        self.assertFalse(graph_color_dfs(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_8(self):
        """Test DFS graph coloring."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 6, 1.0)

        self.assertFalse(graph_color_dfs(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_3(self):
        """Test DFS with pruning for graph coloring."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        self.assertFalse(graph_color_dfs_pruning(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs_pruning(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_4(self):
        """Test DFS with pruning for graph coloring."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(1, 3, 1.0)

        self.assertFalse(graph_color_dfs_pruning(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs_pruning(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_5(self):
        """Test DFS with pruning for graph coloring on Figure 16-7."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        self.assertFalse(graph_color_dfs_pruning(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs_pruning(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_5b(self):
        """Test DFS with pruning for graph coloring on Figure 16-8."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_6(self):
        """Test DFS with pruning for graph coloring"""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)

        self.assertFalse(graph_color_dfs_pruning(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs_pruning(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_dfs_prune_8(self):
        """Test DFS with pruning for graph coloring"""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 6, 1.0)

        self.assertFalse(graph_color_dfs_pruning(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertFalse(graph_color_dfs_pruning(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))

        self.assertTrue(graph_color_dfs_pruning(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))

    def test_removal_3(self):
        """Test the removal algorithm for graph coloring."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        # Create an identical copy to make sure we don't mess up the graph
        g2 = Graph(3, undirected=True)
        g2.insert_edge(0, 1, 1.0)
        g2.insert_edge(1, 2, 1.0)
        g2.insert_edge(2, 0, 1.0)
        self.assertTrue(g2.is_same_structure(g))

        self.assertFalse(graph_color_removal(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

        self.assertFalse(graph_color_removal(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

        self.assertTrue(graph_color_removal(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

    def test_removal_4(self):
        """Test the removal algorithm for graph coloring."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(1, 3, 1.0)

        # Create an identical copy to make sure we don't mess up the graph
        g2 = Graph(4, undirected=True)
        g2.insert_edge(0, 1, 1.0)
        g2.insert_edge(1, 2, 1.0)
        g2.insert_edge(2, 3, 1.0)
        g2.insert_edge(3, 0, 1.0)
        g2.insert_edge(1, 3, 1.0)
        self.assertTrue(g2.is_same_structure(g))

        self.assertFalse(graph_color_removal(g, 1))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

        self.assertFalse(graph_color_removal(g, 2))
        self.assertTrue(g.is_unlabeled())
        self.assertFalse(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

        self.assertTrue(graph_color_removal(g, 3))
        self.assertFalse(g.is_unlabeled())
        self.assertTrue(is_graph_coloring_valid(g))
        self.assertTrue(g2.is_same_structure(g))

    def test_removal_5(self):
        """Test the removal algorithm for graph coloring."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)
        g_copy = g.make_copy()

        self.assertTrue(graph_color_removal(g, 3))
        self.assertTrue(g.is_same_structure(g_copy))

    def test_removal_6(self):
        """Test the removal algorithm for graph coloring."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)

        self.assertTrue(graph_color_removal(g, 3))
        self.assertTrue(is_graph_coloring_valid(g))

        # Reset the labels and add an edge.
        for node in g.nodes:
            node.label = None
        g.insert_edge(2, 5, 1.0)

        self.assertFalse(graph_color_removal(g, 3))
        self.assertFalse(is_graph_coloring_valid(g))

    def test_removal_8(self):
        """Test the removal algorithm for graph coloring."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(0, 5, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(3, 6, 1.0)
        self.assertFalse(is_graph_coloring_valid(g))
        g_copy = g.make_copy()

        self.assertTrue(graph_color_removal(g, 4))
        self.assertTrue(is_graph_coloring_valid(g))
        self.assertTrue(g.is_same_structure(g_copy))


if __name__ == "__main__":
    unittest.main()
