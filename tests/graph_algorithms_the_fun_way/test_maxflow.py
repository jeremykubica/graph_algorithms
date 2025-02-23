import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.maxflow import *


class TestCapacityEdge(unittest.TestCase):
    def test_create(self):
        """Test the creation of a CapacityEdge."""
        e = CapacityEdge(0, 1, 10)
        self.assertEqual(e.to_node, 1)
        self.assertEqual(e.from_node, 0)
        self.assertEqual(e.capacity, 10)
        self.assertEqual(e.used, 0)

    def test_residual(self):
        """Test the computation of a residual."""
        e = CapacityEdge(0, 1, 10)
        e.adjust_used(2)
        self.assertAlmostEqual(e.capacity_left(), 8)
        self.assertAlmostEqual(e.flow_used(), 2)

    def test_capcity_error(self):
        """Test an invalid change to flow."""
        e = CapacityEdge(0, 1, 10)
        with self.assertRaises(Exception):
            e.adjust_used(20)
        with self.assertRaises(Exception):
            e.adjust_used(-2)


class TestResidualGraph(unittest.TestCase):
    def test_create(self):
        """Test the creation of a ResidualGraph."""
        g = ResidualGraph(4, 0, 2)

        # Check we have created a graph for 4 nodes and no edges.
        self.assertEqual(g.num_nodes, 4)
        self.assertEqual(len(g.edges), 4)
        for i in range(4):
            self.assertEqual(len(g.edges[i]), 0)

        # Check that we correctly insert edges.
        g.insert_edge(0, 1, 20)
        g.insert_edge(3, 2, 10)
        self.assertEqual(len(g.edges[0]), 1)
        self.assertEqual(len(g.edges[1]), 0)
        self.assertEqual(len(g.edges[2]), 0)
        self.assertEqual(len(g.edges[3]), 1)
        self.assertAlmostEqual(g.edges[0][1].capacity, 20)
        self.assertAlmostEqual(g.edges[3][2].capacity, 10)

        # Check forward and backward functions.
        for i in range(4):
            for j in range(4):
                is_edge = (i == 0 and j == 1) or (i == 3 and j == 2)
                self.assertEqual(j in g.edges[i], is_edge)

    def test_create_errors(self):
        """Test the errors generated when creating an invalid ResidualGraph."""
        g = ResidualGraph(4, 0, 3)
        g.insert_edge(0, 1, 20)
        g.insert_edge(1, 2, 20)
        g.insert_edge(2, 3, 20)

        # Out of bounds.
        with self.assertRaises(IndexError):
            g.insert_edge(2, 10, 20)
        with self.assertRaises(IndexError):
            g.insert_edge(10, 3, 20)

        # Edge into source.
        with self.assertRaises(ValueError):
            g.insert_edge(2, 0, 20)

        # Edge from sink.
        with self.assertRaises(ValueError):
            g.insert_edge(3, 1, 20)

        # Negative capacity.
        with self.assertRaises(ValueError):
            g.insert_edge(1, 3, -20)

    def test_residuals(self):
        """Test the computation of residuals."""
        g = ResidualGraph(4, 0, 2)
        g.insert_edge(0, 1, 20)
        g.insert_edge(3, 2, 10)
        g.insert_edge(0, 2, 5)
        g.insert_edge(1, 3, 8)
        self.assertEqual(g.compute_total_flow(), 0)

        # Min residual
        min_res = g.min_residual_on_path([-1, 0, 3, 1])
        self.assertAlmostEqual(min_res, 8)

        # Update Path
        g.update_along_path([-1, 0, 3, 1], 2)
        self.assertAlmostEqual(g.get_residual(0, 1), 18)
        self.assertAlmostEqual(g.get_residual(1, 0), 2)
        self.assertAlmostEqual(g.get_residual(0, 2), 5)
        self.assertAlmostEqual(g.get_residual(2, 0), 0)
        self.assertAlmostEqual(g.get_residual(1, 3), 6)
        self.assertAlmostEqual(g.get_residual(3, 1), 2)
        self.assertAlmostEqual(g.get_residual(3, 2), 8)
        self.assertAlmostEqual(g.get_residual(2, 3), 2)
        self.assertEqual(g.compute_total_flow(), 2)

        # Min residual
        min_res = g.min_residual_on_path([-1, 0, 3, 1])
        self.assertAlmostEqual(min_res, 6)

    def test_compute_flow(self):
        """Test that we can compute the total flow as we adjust flow along edges."""
        g = ResidualGraph(4, 0, 3)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 3)
        self.assertEqual(g.compute_total_flow(), 0)

        g.get_edge(0, 1).adjust_used(5)
        g.get_edge(1, 3).adjust_used(5)
        self.assertEqual(g.compute_total_flow(), 5)

        g.get_edge(0, 2).adjust_used(3)
        g.get_edge(2, 3).adjust_used(3)
        self.assertEqual(g.compute_total_flow(), 8)


class TestMaxFlow(unittest.TestCase):
    def test_find_augmenting_path_bfs(self):
        """Test that we can find an augmenting path with BFS."""
        g = ResidualGraph(6, 0, 5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 4)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 4, 3)
        g.insert_edge(2, 5, 2)
        g.insert_edge(3, 2, 2)
        g.insert_edge(3, 4, 5)
        g.insert_edge(4, 5, 3)

        # Find and check the first path.
        last = find_augmenting_path_bfs(g)
        self.assertEqual(last, [-1, 0, 1, 0, 1, 2])
        self.assertEqual(g.min_residual_on_path(last), 1)
        g.update_along_path(last, 1)

        # Find and check the second path.
        last = find_augmenting_path_bfs(g)
        self.assertEqual(last, [-1, 0, 3, 0, 1, 4])
        self.assertEqual(g.min_residual_on_path(last), 3)

    def test_find_augmenting_path_dfs(self):
        """Test that we can find an augmenting path with DFS."""
        g = ResidualGraph(6, 0, 5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 4)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 4, 3)
        g.insert_edge(2, 5, 2)
        g.insert_edge(3, 2, 2)
        g.insert_edge(3, 4, 5)
        g.insert_edge(4, 5, 3)

        # Find and check the first path.
        last = find_augmenting_path_dfs(g)
        self.assertEqual(last, [-1, 0, 1, 0, 1, 2])
        self.assertEqual(g.min_residual_on_path(last), 1)
        g.update_along_path(last, 1)

        # Find and check the second path.
        last = find_augmenting_path_dfs(g)
        self.assertEqual(last, [-1, 0, -1, 0, 1, 4])
        self.assertEqual(g.min_residual_on_path(last), 3)

    def test_find_augmenting_path_dfs2(self):
        """Test that we can find an augmenting path with DFS."""
        g = ResidualGraph(4, 0, 3)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 3)

        # Manually set some values
        g.get_edge(0, 1).adjust_used(5)
        g.get_edge(0, 2).adjust_used(2)
        g.get_edge(1, 2).adjust_used(1)
        g.get_edge(1, 3).adjust_used(4)
        g.get_edge(2, 3).adjust_used(3)

        # Find and check the path.
        last = find_augmenting_path_dfs(g)
        self.assertEqual(last, [-1, 2, 0, 1])
        self.assertEqual(g.min_residual_on_path(last), 1)

    def test_ford_fulkerson_A(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(3)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 2, 5)
        g.insert_edge(1, 2, 1)

        g2 = ford_fulkerson(g, 0, 2)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 1)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 1)

    def test_ford_fulkerson_A_real(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(3)
        g.insert_edge(0, 1, 2.1)
        g.insert_edge(0, 2, 5.3)
        g.insert_edge(1, 2, 1.5)

        g2 = ford_fulkerson(g, 0, 2)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 1.5)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 5.3)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 1.5)

    def test_edmonds_karp_A(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(3)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 2, 5)
        g.insert_edge(1, 2, 1)

        g2 = edmonds_karp(g, 0, 2)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 1)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 1)

    def test_edmonds_karp_A_real(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(3)
        g.insert_edge(0, 1, 2.1)
        g.insert_edge(0, 2, 5.3)
        g.insert_edge(1, 2, 1.5)

        g2 = edmonds_karp(g, 0, 2)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 1.5)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 5.3)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 1.5)

    def test_ford_fulkerson_B(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(6)
        g.insert_edge(0, 1, 10)
        g.insert_edge(0, 3, 5)
        g.insert_edge(1, 2, 8)
        g.insert_edge(1, 3, 5)
        g.insert_edge(2, 5, 10)
        g.insert_edge(3, 4, 8)
        g.insert_edge(4, 2, 2)
        g.insert_edge(4, 5, 6)

        g2 = ford_fulkerson(g, 0, 5)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 10)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 8)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 2)
        self.assertAlmostEqual(g2.get_edge(2, 5).used, 9)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 7)
        self.assertAlmostEqual(g2.get_edge(4, 2).used, 1)
        self.assertAlmostEqual(g2.get_edge(4, 5).used, 6)

    def test_edmonds_karp_B(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(6)
        g.insert_edge(0, 1, 10)
        g.insert_edge(0, 3, 5)
        g.insert_edge(1, 2, 8)
        g.insert_edge(1, 3, 5)
        g.insert_edge(2, 5, 10)
        g.insert_edge(3, 4, 8)
        g.insert_edge(4, 2, 2)
        g.insert_edge(4, 5, 6)

        g2 = edmonds_karp(g, 0, 5)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 10)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 8)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 2)
        self.assertAlmostEqual(g2.get_edge(2, 5).used, 9)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 7)
        self.assertAlmostEqual(g2.get_edge(4, 2).used, 1)
        self.assertAlmostEqual(g2.get_edge(4, 5).used, 6)

    def test_ford_fulkerson_C(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 10)
        g.insert_edge(3, 1, 3)
        g.insert_edge(1, 2, 6)
        g.insert_edge(2, 4, 10)
        g.insert_edge(3, 4, 5)

        g2 = ford_fulkerson(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 11)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 6)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 6)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 5)
        self.assertAlmostEqual(g2.get_edge(2, 4).used, 6)

    def test_ford_fulkerson_C_real(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 10)
        g.insert_edge(3, 1, 3)
        g.insert_edge(1, 2, 6.25)
        g.insert_edge(2, 4, 10)
        g.insert_edge(3, 4, 5.1)

        g2 = ford_fulkerson(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 11.35)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 6.35)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 6.25)
        self.assertAlmostEqual(g2.get_edge(3, 1).used, 1.25)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 5.1)
        self.assertAlmostEqual(g2.get_edge(2, 4).used, 6.25)

    def test_edmonds_karp_C(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 10)
        g.insert_edge(3, 1, 3)
        g.insert_edge(1, 2, 6)
        g.insert_edge(2, 4, 10)
        g.insert_edge(3, 4, 5)

        g2 = edmonds_karp(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 11)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 6)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 6)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 5)
        self.assertAlmostEqual(g2.get_edge(2, 4).used, 6)

    def test_edmonds_karp_C_real(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 3, 10)
        g.insert_edge(3, 1, 3)
        g.insert_edge(1, 2, 6.25)
        g.insert_edge(2, 4, 10)
        g.insert_edge(3, 4, 5.1)

        g2 = edmonds_karp(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 11.35)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 6.35)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 6.25)
        self.assertAlmostEqual(g2.get_edge(3, 1).used, 1.25)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 5.1)
        self.assertAlmostEqual(g2.get_edge(2, 4).used, 6.25)

    def test_ford_fulkerson_D(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(4)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(2, 1, 5)
        g.insert_edge(1, 3, 7)
        g.insert_edge(2, 3, 5)

        g2 = ford_fulkerson(g, 0, 3)
        self.assertEqual(g2.compute_total_flow(), 12)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 7)
        self.assertAlmostEqual(g2.get_edge(2, 1).used, 2)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 7)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 5)

    def test_edmonds_karp_D(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(4)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(2, 1, 5)
        g.insert_edge(1, 3, 7)
        g.insert_edge(2, 3, 5)

        g2 = edmonds_karp(g, 0, 3)
        self.assertEqual(g2.compute_total_flow(), 12)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 7)
        self.assertAlmostEqual(g2.get_edge(2, 1).used, 2)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 7)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 5)

    def test_ford_fulkerson_E(self):
        """Test the DFS Ford-Fulkerson implementation from Figure 14-12."""
        g = Graph(8)
        g.insert_edge(0, 1, 8)
        g.insert_edge(0, 3, 1)
        g.insert_edge(0, 5, 10)
        g.insert_edge(1, 2, 7)
        g.insert_edge(2, 7, 3)
        g.insert_edge(2, 3, 5)
        g.insert_edge(3, 4, 8)
        g.insert_edge(4, 7, 7)
        g.insert_edge(5, 4, 10)
        g.insert_edge(5, 6, 7)
        g.insert_edge(6, 7, 5)

        g2 = ford_fulkerson(g, 0, 7)
        self.assertEqual(g2.compute_total_flow(), 15)

    def test_edmonds_karp_E(self):
        """Test the Edmonds-Karp implementation from Figure 14-12."""
        g = Graph(8)
        g.insert_edge(0, 1, 8)
        g.insert_edge(0, 3, 1)
        g.insert_edge(0, 5, 10)
        g.insert_edge(1, 2, 7)
        g.insert_edge(2, 7, 3)
        g.insert_edge(2, 3, 5)
        g.insert_edge(3, 4, 8)
        g.insert_edge(4, 7, 7)
        g.insert_edge(5, 4, 10)
        g.insert_edge(5, 6, 7)
        g.insert_edge(6, 7, 5)

        g2 = edmonds_karp(g, 0, 7)
        self.assertEqual(g2.compute_total_flow(), 15)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 4)
        self.assertAlmostEqual(g2.get_edge(0, 3).used, 1)
        self.assertAlmostEqual(g2.get_edge(0, 5).used, 10)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 4)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 1)
        self.assertAlmostEqual(g2.get_edge(2, 7).used, 3)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 2)
        self.assertAlmostEqual(g2.get_edge(4, 7).used, 7)
        self.assertAlmostEqual(g2.get_edge(5, 4).used, 5)
        self.assertAlmostEqual(g2.get_edge(5, 6).used, 5)
        self.assertAlmostEqual(g2.get_edge(6, 7).used, 5)

    def test_ford_fulkerson_F(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(4)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 3)

        g2 = ford_fulkerson(g, 0, 3)
        self.assertEqual(g2.compute_total_flow(), 8)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 0)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 3)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 3)

    def test_edmonds_karp_F(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(4)
        g.insert_edge(0, 1, 5)
        g.insert_edge(0, 2, 10)
        g.insert_edge(1, 2, 1)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 3)

        g2 = edmonds_karp(g, 0, 3)
        self.assertEqual(g2.compute_total_flow(), 8)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 0)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 3)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 3)

    def test_ford_fulkerson_G(self):
        """Test the DFS Ford-Fulkerson implementation on the graph in Figure 14-10."""
        g: Graph = Graph(7)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 2, 5)
        g.insert_edge(0, 3, 1)
        g.insert_edge(1, 3, 2)
        g.insert_edge(1, 4, 7)
        g.insert_edge(2, 3, 5)
        g.insert_edge(2, 5, 3)
        g.insert_edge(3, 6, 8)
        g.insert_edge(4, 6, 4)
        g.insert_edge(5, 6, 5)

        residual_graph: Graph = ford_fulkerson(g, 0, 6)
        self.assertEqual(residual_graph.compute_total_flow(), 9)
        self.assertAlmostEqual(residual_graph.get_edge(0, 1).used, 3)
        self.assertAlmostEqual(residual_graph.get_edge(0, 2).used, 5)
        self.assertAlmostEqual(residual_graph.get_edge(0, 3).used, 1)
        self.assertAlmostEqual(residual_graph.get_edge(1, 3).used, 1)
        self.assertAlmostEqual(residual_graph.get_edge(1, 4).used, 2)
        self.assertAlmostEqual(residual_graph.get_edge(2, 3).used, 5)
        self.assertAlmostEqual(residual_graph.get_edge(2, 5).used, 0)
        self.assertAlmostEqual(residual_graph.get_edge(3, 6).used, 7)
        self.assertAlmostEqual(residual_graph.get_edge(4, 6).used, 2)
        self.assertAlmostEqual(residual_graph.get_edge(5, 6).used, 0)

    def test_ford_fulkerson_H(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 2, 1)
        g.insert_edge(0, 3, 5)
        g.insert_edge(1, 2, 2)
        g.insert_edge(1, 4, 4)
        g.insert_edge(2, 4, 8)
        g.insert_edge(3, 2, 5)
        g.insert_edge(3, 4, 5)
        g2 = ford_fulkerson(g, 0, 4)

    def test_ford_fulkerson_I(self):
        """Test the DFS Ford-Fulkerson implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 2, 3)
        g.insert_edge(1, 2, 10)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 8)
        g.insert_edge(3, 4, 1)

        g2 = ford_fulkerson(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 1)

        g.insert_edge(3, 4, 5)
        g2 = ford_fulkerson(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 5)

        g.insert_edge(0, 4, 5)
        g2 = ford_fulkerson(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 10)

    def test_edmonds_karp_I(self):
        """Test the Edmonds-Karp implementation."""
        g = Graph(5)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 2, 3)
        g.insert_edge(1, 2, 10)
        g.insert_edge(1, 3, 10)
        g.insert_edge(2, 3, 8)
        g.insert_edge(3, 4, 1)

        g2 = edmonds_karp(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 1)

        g.insert_edge(3, 4, 5)
        g2 = edmonds_karp(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 5)

        g.insert_edge(0, 4, 5)
        g2 = edmonds_karp(g, 0, 4)
        self.assertEqual(g2.compute_total_flow(), 10)

    def test_multi_source(self):
        """Test the transformation of a multi-source graph."""
        g = Graph(4)
        g.insert_edge(0, 2, 8)
        g.insert_edge(1, 2, 5)
        g.insert_edge(2, 3, 10)

        # Add a super source
        new_source_ind = augment_multisource_graph(g, [0, 1])
        self.assertEqual(g.num_nodes, 5)

        g2 = ford_fulkerson(g, new_source_ind, 3)
        self.assertAlmostEqual(g2.get_edge(0, 2).used, 8)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 2)
        self.assertAlmostEqual(g2.get_edge(2, 3).used, 10)

    def test_multi_sink(self):
        """Test the transformation of a multi-sink graph."""
        g = Graph(4)
        g.insert_edge(0, 1, 10)
        g.insert_edge(1, 2, 5)
        g.insert_edge(1, 3, 8)

        # Add a super sink
        new_sink_ind = augment_multisink_graph(g, [2, 3])
        self.assertEqual(g.num_nodes, 5)

        g2 = ford_fulkerson(g, 0, new_sink_ind)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 10)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 3).used, 5)

    def test_multi_source_multi_sink(self):
        """Test the transformation of a multi-source, multi-sink graph."""
        g = Graph(6)
        g.insert_edge(0, 1, 2)
        g.insert_edge(1, 2, 5)
        g.insert_edge(1, 5, 2)
        g.insert_edge(3, 1, 5)
        g.insert_edge(3, 4, 4)
        g.insert_edge(4, 5, 3)

        # Add a super source
        new_source_ind = augment_multisource_graph(g, [0, 3])
        self.assertEqual(g.num_nodes, 7)
        self.assertIsNotNone(g.get_edge(new_source_ind, 0))
        self.assertIsNotNone(g.get_edge(new_source_ind, 3))

        # Add a super sink
        new_sink_ind = augment_multisink_graph(g, [2, 5])
        self.assertEqual(g.num_nodes, 8)
        self.assertIsNotNone(g.get_edge(2, new_sink_ind))
        self.assertIsNotNone(g.get_edge(5, new_sink_ind))

        g2 = ford_fulkerson(g, new_source_ind, new_sink_ind)
        self.assertAlmostEqual(g2.get_edge(0, 1).used, 2)
        self.assertAlmostEqual(g2.get_edge(1, 2).used, 5)
        self.assertAlmostEqual(g2.get_edge(1, 5).used, 2)
        self.assertAlmostEqual(g2.get_edge(3, 4).used, 3)
        self.assertAlmostEqual(g2.get_edge(3, 1).used, 5)
        self.assertAlmostEqual(g2.get_edge(4, 5).used, 3)


if __name__ == "__main__":
    unittest.main()
