import unittest

from graph_algorithms_the_fun_way.graph import Edge, Graph
from graph_algorithms_the_fun_way.paths import *


class TestGrapPaths(unittest.TestCase):
    def setUp(self):
        """Set up data to be used throughout the tests."""
        self.g1 = Graph(1, undirected=False)

        self.g2 = Graph(2, undirected=True)
        self.g2.insert_edge(0, 1, 1.0)

        self.g3 = Graph(3, undirected=True)
        self.g3.insert_edge(0, 1, 1.0)
        self.g3.insert_edge(0, 2, 2.0)
        self.g3.insert_edge(1, 2, 0.8)

        self.g4 = Graph(4, undirected=False)
        self.g4.insert_edge(0, 1, 1.0)
        self.g4.insert_edge(1, 0, 1.0)
        self.g4.insert_edge(0, 2, 1.0)
        self.g4.insert_edge(2, 0, 1.0)
        self.g4.insert_edge(1, 3, 1.0)
        self.g4.insert_edge(3, 1, 1.0)
        self.g4.insert_edge(2, 3, 0.5)
        self.g4.insert_edge(3, 2, 1.0)

        self.g5 = Graph(5, undirected=False)
        self.g5.insert_edge(0, 1, 1.0)
        self.g5.insert_edge(1, 0, 1.0)
        self.g5.insert_edge(0, 2, 1.0)
        self.g5.insert_edge(2, 3, 2.0)
        self.g5.insert_edge(1, 3, 1.0)
        self.g5.insert_edge(3, 1, 1.0)
        self.g5.insert_edge(3, 4, 0.5)
        self.g5.insert_edge(4, 1, 1.0)

        self.g6 = Graph(6, undirected=False)
        self.g6.insert_edge(0, 1, 5.0)
        self.g6.insert_edge(0, 3, 1.0)
        self.g6.insert_edge(0, 4, 2.5)
        self.g6.insert_edge(1, 0, 4.0)
        self.g6.insert_edge(1, 2, 1.0)
        self.g6.insert_edge(2, 1, 3.0)
        self.g6.insert_edge(3, 4, 3.0)
        self.g6.insert_edge(4, 1, 1.0)
        self.g6.insert_edge(4, 2, 5.0)
        self.g6.insert_edge(4, 3, 1.0)
        self.g6.insert_edge(4, 5, 2.0)
        self.g6.insert_edge(5, 2, 1.0)
        self.g6.insert_edge(5, 4, 1.0)

    def test_check_path_valid_last_1(self):
        """Test check_last_path_valid on a graph of size 1."""
        self.assertEqual(True, check_last_path_valid(self.g1, [-1]))
        self.assertEqual(False, check_last_path_valid(self.g1, [0]))

    def test_check_path_valid_last_3(self):
        """Test check_last_path_valid on a graph of size 3."""
        self.assertEqual(False, check_last_path_valid(self.g3, []))
        self.assertEqual(True, check_last_path_valid(self.g3, [-1, -1, -1]))
        self.assertEqual(True, check_last_path_valid(self.g3, [-1, 0, 1]))
        self.assertEqual(True, check_last_path_valid(self.g3, [2, -1, 1]))

    def test_check_path_valid_last_5(self):
        """Test check_last_path_valid on a graph of size 5."""
        self.assertEqual(False, check_last_path_valid(self.g5, []))
        self.assertEqual(False, check_last_path_valid(self.g5, [-1, -1, -1, -1]))
        self.assertEqual(False, check_last_path_valid(self.g5, [-1, -1, -1, -1, -1, -1]))
        self.assertEqual(True, check_last_path_valid(self.g5, [-1, -1, -1, -1, -1]))

        self.assertEqual(True, check_last_path_valid(self.g5, [-1, 0, -1, 1, 3]))
        self.assertEqual(True, check_last_path_valid(self.g5, [1, 3, -1, 2, -1]))
        self.assertEqual(True, check_last_path_valid(self.g5, [1, -1, 0, -1, -1]))

        self.assertEqual(False, check_last_path_valid(self.g5, [-1, 0, 2, 1, 3]))
        self.assertEqual(False, check_last_path_valid(self.g5, [1, 3, -1, 2, 2]))
        self.assertEqual(False, check_last_path_valid(self.g5, [4, -1, 0, -1, -1]))

    def test_check_path_valid_nodes_1(self):
        """Test check_node_path_valid on a graph of size 1."""
        self.assertEqual(True, check_node_path_valid(self.g1, []))
        self.assertEqual(True, check_node_path_valid(self.g1, [0]))

    def test_check_path_valid_nodes_3(self):
        """Test check_node_path_valid on a graph of size 3."""
        self.assertEqual(True, check_node_path_valid(self.g3, []))
        self.assertEqual(True, check_node_path_valid(self.g3, [0]))
        self.assertEqual(True, check_node_path_valid(self.g3, [0, 1, 2]))
        self.assertEqual(True, check_node_path_valid(self.g3, [2, 0, 1]))
        self.assertEqual(True, check_node_path_valid(self.g3, [2, 0, 1, 0]))
        self.assertEqual(True, check_node_path_valid(self.g3, [2, 0, 1, 2, 0, 1]))
        self.assertEqual(False, check_node_path_valid(self.g3, [3]))
        self.assertEqual(False, check_node_path_valid(self.g3, [2, 1, 1]))
        self.assertEqual(False, check_node_path_valid(self.g3, [2, 2]))

    def test_check_path_valid_nodes_5(self):
        """Test check_node_path_valid on a graph of size 5."""
        self.assertEqual(True, check_node_path_valid(self.g5, []))
        self.assertEqual(True, check_node_path_valid(self.g5, [0]))
        self.assertEqual(False, check_node_path_valid(self.g5, [0, 1, 2]))
        self.assertEqual(True, check_node_path_valid(self.g5, [0, 1, 0, 2, 3, 4, 1, 3]))
        self.assertEqual(False, check_node_path_valid(self.g5, [0, 1, 0, 2, 3, 4, 1, 2]))
        self.assertEqual(False, check_node_path_valid(self.g5, [0, 2, 0, 2, 3, 4, 1, 3]))

    def test_check_path_valid_edges_1(self):
        """Test check_edge_path_valid on a graph of size 1."""
        self.assertEqual(True, check_edge_path_valid(self.g1, []))

    def test_check_path_valid_edges_3(self):
        """Test check_edge_path_valid on a graph of size 3."""
        self.assertEqual(True, check_edge_path_valid(self.g3, []))
        self.assertEqual(True, check_edge_path_valid(self.g3, [Edge(0, 1, 1.0), Edge(1, 2, 1.0)]))
        self.assertEqual(True, check_edge_path_valid(self.g3, [Edge(2, 0, 1.0), Edge(0, 1, 1.0)]))
        self.assertEqual(
            True, check_edge_path_valid(self.g3, [Edge(2, 0, 1.0), Edge(0, 1, 1.0), Edge(1, 0, 1.0)])
        )
        self.assertEqual(
            True,
            check_edge_path_valid(
                self.g3, [Edge(2, 0, 1.0), Edge(0, 1, 1.0), Edge(1, 2, 1.0), Edge(2, 0, 1.0), Edge(0, 1, 1.0)]
            ),
        )

        self.assertEqual(False, check_edge_path_valid(self.g3, [Edge(3, 0, 1.0)]))
        self.assertEqual(False, check_edge_path_valid(self.g3, [Edge(2, 1, 1.0), Edge(1, 1, 1.0)]))
        self.assertEqual(False, check_edge_path_valid(self.g3, [Edge(2, 2, 1.0)]))
        self.assertEqual(
            False,
            check_edge_path_valid(
                self.g3, [Edge(2, 0, 1.0), Edge(0, 1, 1.0), Edge(2, 0, 1.0), Edge(0, 1, 1.0)]
            ),
        )

    def test_check_path_valid_edges_5(self):
        """Test check_edge_path_valid on a graph of size 5."""
        self.assertEqual(True, check_edge_path_valid(self.g5, []))
        self.assertEqual(False, check_edge_path_valid(self.g5, [Edge(0, 1, 1.0), Edge(1, 2, 1.0)]))
        self.assertEqual(
            True,
            check_edge_path_valid(
                self.g5, [Edge(2, 3, 1.0), Edge(3, 4, 1.0), Edge(4, 1, 1.0), Edge(1, 0, 1.0)]
            ),
        )
        self.assertEqual(
            True,
            check_edge_path_valid(
                self.g5,
                [
                    Edge(0, 1, 1.0),
                    Edge(1, 0, 1.0),
                    Edge(0, 2, 1.0),
                    Edge(2, 3, 1.0),
                    Edge(3, 4, 1.0),
                    Edge(4, 1, 1.0),
                    Edge(1, 3, 1.0),
                ],
            ),
        )
        self.assertEqual(
            False,
            check_edge_path_valid(
                self.g5,
                [
                    Edge(0, 1, 1.0),
                    Edge(0, 2, 1.0),
                    Edge(2, 3, 1.0),
                    Edge(3, 4, 1.0),
                    Edge(4, 1, 1.0),
                    Edge(1, 3, 1.0),
                    Edge(2, 0, 1.0),
                ],
            ),
        )
        self.assertEqual(
            False,
            check_edge_path_valid(
                self.g5,
                [
                    Edge(0, 1, 1.0),
                    Edge(1, 0, 1.0),
                    Edge(0, 2, 1.0),
                    Edge(2, 3, 1.0),
                    Edge(3, 4, 1.0),
                    Edge(1, 3, 1.0),
                    Edge(2, 0, 1.0),
                ],
            ),
        )
        self.assertEqual(
            False,
            check_edge_path_valid(
                self.g5,
                [
                    Edge(0, 1, 1.0),
                    Edge(1, 0, 1.0),
                    Edge(0, 2, 1.0),
                    Edge(2, 3, 1.0),
                    Edge(3, 4, 1.0),
                    Edge(4, 1, 1.0),
                    Edge(1, 2, 1.0),
                ],
            ),
        )
        self.assertEqual(
            False,
            check_edge_path_valid(
                self.g5,
                [
                    Edge(0, 2, 1.0),
                    Edge(2, 0, 1.0),
                    Edge(0, 2, 1.0),
                    Edge(2, 3, 1.0),
                    Edge(3, 4, 1.0),
                    Edge(4, 1, 1.0),
                    Edge(1, 3, 1.0),
                ],
            ),
        )

    def test_edge_path_to_node_path(self):
        """Test that we can convert an edge path to a node path."""
        self.assertEqual(edge_path_to_node_path([]), [])
        self.assertEqual(edge_path_to_node_path([Edge(0, 1, 1.0)]), [0, 1])
        self.assertEqual(
            edge_path_to_node_path(
                [Edge(0, 1, 1.0), Edge(1, 2, 1.0), Edge(2, 0, 1.0), Edge(0, 3, 1.0), Edge(3, 2, 1.0)]
            ),
            [0, 1, 2, 0, 3, 2],
        )
        self.assertEqual(
            edge_path_to_node_path(
                [
                    Edge(8, 1, 1.0),
                    Edge(1, 8, 1.0),
                    Edge(8, 0, 1.0),
                    Edge(0, 8, 1.0),
                    Edge(8, 2, 1.0),
                    Edge(2, 3, 1.0),
                ]
            ),
            [8, 1, 8, 0, 8, 2, 3],
        )
        with self.assertRaises(ValueError):
            edge_path_to_node_path([Edge(0, 1, 1.0), Edge(1, 2, 1.0), Edge(0, 3, 1.0), Edge(3, 2, 1.0)])

    def test_node_path_to_edge_path(self):
        """Test that we can convert a node path to an edge path."""
        path = [8, 1, 8, 0, 8, 2, 3]
        result = node_path_to_edge_path(path)
        self.assertEqual(len(result), 6)

        for i in range(0, len(result)):
            self.assertEqual(result[i].from_node, path[i])
            self.assertEqual(result[i].to_node, path[i + 1])
            self.assertEqual(result[i].weight, 1.0)

        path = [1, 2, 3, 4, 4, 5, 4, 3, 2, 1]
        result = node_path_to_edge_path(path)
        self.assertEqual(len(result), 9)

        for i in range(0, len(result)):
            self.assertEqual(result[i].from_node, path[i])
            self.assertEqual(result[i].to_node, path[i + 1])
            self.assertEqual(result[i].weight, 1.0)

    def test_make_node_path_from_last(self):
        """Test that we can convert a last path to a node path."""
        last = [-1, 4, 0, 2, 3]
        self.assertEqual(make_node_path_from_last(last, 4), [0, 2, 3, 4])
        self.assertEqual(make_node_path_from_last(last, 1), [0, 2, 3, 4, 1])
        self.assertEqual(make_node_path_from_last(last, 0), [0])

        last = [4, -1, 3, 1, 3]
        self.assertEqual(make_node_path_from_last(last, 4), [1, 3, 4])
        self.assertEqual(make_node_path_from_last(last, 0), [1, 3, 4, 0])
        self.assertEqual(make_node_path_from_last(last, 1), [1])
        self.assertEqual(make_node_path_from_last(last, 2), [1, 3, 2])

        last = [-1, 0, 1, 2, 2, 0, 5, 0, 5, 8]
        self.assertEqual(make_node_path_from_last(last, 4), [0, 1, 2, 4])
        self.assertEqual(make_node_path_from_last(last, 9), [0, 5, 8, 9])
        self.assertEqual(make_node_path_from_last(last, 3), [0, 1, 2, 3])
        self.assertEqual(make_node_path_from_last(last, 7), [0, 7])
        self.assertEqual(make_node_path_from_last(last, 0), [0])

    def test_check_path_cost_3(self):
        """Test that we can compute path costs on a graph of size 3."""
        self.assertEqual(compute_path_cost(self.g3, [0]), 0.0)
        self.assertEqual(compute_path_cost(self.g3, [0, 1, 2]), 1.8)
        self.assertEqual(compute_path_cost(self.g3, [2, 0, 1, 2]), 3.8)
        self.assertEqual(compute_path_cost(self.g3, [2, 0, 1]), 3.0)

    def test_check_path_cost_5(self):
        """Test that we can compute path costs on a graph of size 5."""
        self.assertEqual(compute_path_cost(self.g5, []), 0.0)
        self.assertEqual(compute_path_cost(self.g5, [0]), 0.0)
        self.assertEqual(compute_path_cost(self.g5, [0, 1, 0]), 2.0)
        self.assertEqual(compute_path_cost(self.g5, [0, 1, 3, 4]), 2.5)
        self.assertEqual(compute_path_cost(self.g5, [0, 2, 3, 1, 3, 4, 1]), 6.5)
        self.assertEqual(compute_path_cost(self.g5, [0, 1, 3, 4, 1]), 3.5)

    def test_check_path_cost_figure_3_6(self):
        """Test that we can compute path costs the graph from Figure 3.6"""
        self.assertEqual(compute_path_cost(self.g6, [0, 3, 4, 2]), 9.0)

    # --- Functions for Hamiltonian Paths ----------------------
    def test_check_hamiltonian_path_1(self):
        self.assertEqual(is_hamiltonian_path(self.g1, []), False)
        self.assertEqual(is_hamiltonian_path(self.g1, [0]), True)

    def test_check_hamiltonian_path_3(self):
        self.assertEqual(is_hamiltonian_path(self.g3, []), False)
        self.assertEqual(is_hamiltonian_path(self.g3, [0]), False)
        self.assertEqual(is_hamiltonian_path(self.g3, [0, 1, 2]), True)
        self.assertEqual(is_hamiltonian_path(self.g3, [2, 0, 1, 2]), False)
        self.assertEqual(is_hamiltonian_path(self.g3, [2, 0, 1]), True)
        self.assertEqual(is_hamiltonian_path(self.g3, [2, 0, 1, 2]), False)
        self.assertEqual(is_hamiltonian_path(self.g3, [2, 0]), False)

    def test_check_hamiltonian_path_4(self):
        self.assertEqual(is_hamiltonian_path(self.g4, []), False)
        self.assertEqual(is_hamiltonian_path(self.g4, [0]), False)
        self.assertEqual(is_hamiltonian_path(self.g4, [0, 1, 2]), False)
        self.assertEqual(is_hamiltonian_path(self.g4, [2, 0, 1, 3]), True)
        self.assertEqual(is_hamiltonian_path(self.g4, [3, 1, 0, 2]), True)
        self.assertEqual(is_hamiltonian_path(self.g4, [3, 1, 2, 0]), False)
        self.assertEqual(is_hamiltonian_path(self.g4, [0, 1, 3, 2, 0]), False)

    def test_check_hamiltonian_path_5(self):
        self.assertEqual(is_hamiltonian_path(self.g5, [0]), False)
        self.assertEqual(is_hamiltonian_path(self.g5, [2, 0, 1]), False)
        self.assertEqual(is_hamiltonian_path(self.g5, [1, 0, 2, 3, 4]), True)
        self.assertEqual(is_hamiltonian_path(self.g5, [3, 4, 1, 0, 2]), True)
        self.assertEqual(is_hamiltonian_path(self.g5, [0, 2, 1, 3, 4]), False)
        self.assertEqual(is_hamiltonian_path(self.g5, [0, 2, 3, 1, 3, 4]), False)

    def test_hamilton_dfs_1(self):
        """Test a DFS to find Hamiltonian paths."""
        res = hamiltonian_dfs(self.g1)
        self.assertEqual(res, [0])

    def test_hamilton_dfs_3(self):
        """Test a DFS to find Hamiltonian paths."""
        res = hamiltonian_dfs(self.g3)
        self.assertEqual(res, [0, 1, 2])

    def test_hamilton_dfs_3b(self):
        """Test a DFS to find Hamiltonian paths."""
        g3b = Graph(3, undirected=True)
        g3b.insert_edge(0, 1, 1.0)
        g3b.insert_edge(0, 2, 2.0)

        res = hamiltonian_dfs(g3b)
        self.assertEqual(res, [1, 0, 2])

    def test_hamilton_dfs_4(self):
        """Test a DFS to find Hamiltonian paths."""
        res = hamiltonian_dfs(self.g4)
        self.assertEqual(res, [0, 1, 3, 2])

    def test_hamilton_dfs_4b(self):
        """Test a DFS to find Hamiltonian paths."""
        g4b = Graph(4, undirected=True)
        g4b.insert_edge(0, 1, 5.0)
        g4b.insert_edge(1, 2, 6.0)
        g4b.insert_edge(1, 3, 2.0)
        res = hamiltonian_dfs(g4b)
        self.assertIsNone(res)

        g4b.insert_edge(0, 2, 2.0)
        res = hamiltonian_dfs(g4b)
        self.assertEqual(res, [0, 2, 1, 3])

    def test_hamilton_dfs_5(self):
        """Test a DFS to find Hamiltonian paths."""
        g5 = Graph(5, undirected=True)
        g5.insert_edge(0, 3, 5.0)
        g5.insert_edge(3, 1, 6.0)
        g5.insert_edge(1, 4, 6.0)
        g5.insert_edge(1, 2, 6.0)
        res = hamiltonian_dfs(g5)
        self.assertIsNone(res)

        g5.insert_edge(0, 1, 6.0)
        res = hamiltonian_dfs(g5)
        self.assertIsNone(res)

        g5.insert_edge(4, 2, 6.0)
        res = hamiltonian_dfs(g5)
        self.assertEqual(res, [0, 3, 1, 4, 2])

    def test_hamilton_dfs_5b(self):
        """Test a DFS to find Hamiltonian paths."""
        g5 = Graph(5, undirected=True)
        g5.insert_edge(0, 3, 5.0)
        g5.insert_edge(0, 1, 5.0)
        g5.insert_edge(0, 4, 5.0)
        g5.insert_edge(1, 2, 5.0)
        res = hamiltonian_dfs(g5)
        self.assertIsNone(res)

        g5.insert_edge(3, 4, 6.0)
        res = hamiltonian_dfs(g5)
        self.assertEqual(res, [2, 1, 0, 3, 4])

    def test_hamilton_dfs_5c(self):
        """Test a DFS to find Hamiltonian paths on Figure 18-4."""
        g5 = Graph(5, undirected=False)
        g5.insert_edge(0, 1, 1.0)
        g5.insert_edge(1, 0, 1.0)
        g5.insert_edge(1, 2, 1.0)
        g5.insert_edge(1, 3, 1.0)
        g5.insert_edge(2, 0, 1.0)
        g5.insert_edge(2, 3, 1.0)
        g5.insert_edge(2, 4, 1.0)
        g5.insert_edge(3, 2, 1.0)

        res = hamiltonian_dfs(g5)
        self.assertEqual(res, [0, 1, 3, 2, 4])

    def test_hamilton_dfs_6(self):
        """Test a DFS to find Hamiltonian paths."""
        g6 = Graph(6, undirected=True)
        g6.insert_edge(0, 1, 5.0)
        g6.insert_edge(0, 2, 6.0)
        g6.insert_edge(0, 3, 2.0)
        g6.insert_edge(1, 2, 3.0)
        g6.insert_edge(1, 3, 1.0)
        g6.insert_edge(1, 4, 1.0)
        g6.insert_edge(1, 5, 2.0)
        g6.insert_edge(2, 5, 6.0)
        g6.insert_edge(3, 4, 7.0)
        g6.insert_edge(3, 5, 5.0)
        g6.insert_edge(4, 5, 1.0)

        res = hamiltonian_dfs(g6)
        self.assertEqual(res, [0, 1, 2, 5, 3, 4])

    def test_hamilton_dfs_6b(self):
        """Test a DFS to find Hamiltonian paths."""
        g6 = Graph(6, undirected=True)
        g6.insert_edge(0, 1, 5.0)
        g6.insert_edge(0, 3, 6.0)
        g6.insert_edge(1, 2, 3.0)
        g6.insert_edge(1, 3, 1.0)
        g6.insert_edge(1, 4, 1.0)
        g6.insert_edge(1, 5, 2.0)
        g6.insert_edge(2, 5, 6.0)

        res = hamiltonian_dfs(g6)
        self.assertIsNone(res)

    # --- Functions for TSP ---------------------------------
    def test_tsp_1(self):
        """Test DFS for TSP."""
        (score, res) = tsp_dfs(self.g1)
        self.assertEqual(score, 0.0)
        self.assertEqual(res, [0])

    def test_tsp_3(self):
        """Test DFS for TSP."""
        (score, res) = tsp_dfs(self.g3)
        self.assertEqual(score, 3.8)
        self.assertEqual(res, [0, 1, 2, 0])

    def test_tsp_3b(self):
        """Test DFS for TSP."""
        g3b = Graph(3, undirected=True)
        g3b.insert_edge(0, 1, 1.0)
        g3b.insert_edge(0, 2, 2.0)

        (score, res) = tsp_dfs(g3b)
        self.assertEqual(score, math.inf)
        self.assertEqual(res, [])

    def test_tsp_4(self):
        """Test DFS for TSP."""
        (score, res) = tsp_dfs(self.g4)
        self.assertEqual(score, 3.5)
        self.assertEqual(res, [0, 2, 3, 1, 0])

    def test_tsp_4b(self):
        """Test DFS for TSP."""
        g4b = Graph(4, undirected=True)
        g4b.insert_edge(0, 1, 5.0)
        g4b.insert_edge(1, 2, 6.0)
        g4b.insert_edge(1, 3, 2.0)

        (score, res) = tsp_dfs(g4b)
        self.assertEqual(score, math.inf)
        self.assertEqual(res, [])

        g4b.insert_edge(0, 3, 2.0)
        (score, res) = tsp_dfs(g4b)
        self.assertEqual(score, math.inf)
        self.assertEqual(res, [])

        g4b.insert_edge(3, 2, 4.0)
        (score, res) = tsp_dfs(g4b)
        self.assertEqual(score, 17.0)
        self.assertEqual(res, [0, 1, 2, 3, 0])

        g4b.insert_edge(0, 2, 1.0)
        (score, res) = tsp_dfs(g4b)
        self.assertEqual(score, 11.0)
        self.assertEqual(res, [0, 3, 1, 2, 0])

    def test_tsp_5(self):
        """Test DFS for TSP."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        (score, res) = tsp_dfs(g)
        self.assertEqual(score, math.inf)
        self.assertEqual(res, [])

        g.insert_edge(1, 2, 5.0)
        g.insert_edge(2, 3, 5.0)
        g.insert_edge(3, 4, 5.0)
        (score, res) = tsp_dfs(g)
        self.assertEqual(score, 17.0)
        self.assertEqual(res, [0, 1, 2, 3, 4, 0])

        g.insert_edge(1, 3, 1.0)
        (score, res) = tsp_dfs(g)
        self.assertEqual(res, [0, 2, 1, 3, 4, 0])
        self.assertEqual(score, 13.0)

        g.insert_edge(1, 3, 1.0)
        (score, res) = tsp_dfs(g)
        self.assertEqual(res, [0, 2, 1, 3, 4, 0])
        self.assertEqual(score, 13.0)

        g.insert_edge(2, 4, 3.0)
        (score, res) = tsp_dfs(g)
        self.assertEqual(res, [0, 1, 3, 2, 4, 0])
        self.assertEqual(score, 11.0)

    def test_tsp_6(self):
        g6 = Graph(6, undirected=True)
        g6.insert_edge(0, 1, 5.0)
        g6.insert_edge(0, 2, 6.0)
        g6.insert_edge(0, 3, 2.0)
        g6.insert_edge(1, 2, 3.0)
        g6.insert_edge(1, 3, 1.0)
        g6.insert_edge(1, 4, 1.0)
        g6.insert_edge(1, 5, 2.0)
        g6.insert_edge(2, 5, 6.0)
        g6.insert_edge(3, 4, 7.0)
        g6.insert_edge(3, 5, 5.0)
        g6.insert_edge(4, 5, 1.0)

        (score, res) = tsp_dfs(g6)
        self.assertEqual(score, 17.0)
        self.assertEqual(res, [0, 2, 5, 4, 1, 3, 0])

    def test_tsp_6b(self):
        """Test DFS for TSP."""
        g6 = Graph(6, undirected=True)
        g6.insert_edge(0, 1, 5.0)
        g6.insert_edge(0, 3, 6.0)
        g6.insert_edge(1, 2, 3.0)
        g6.insert_edge(1, 3, 1.0)
        g6.insert_edge(1, 4, 1.0)
        g6.insert_edge(1, 5, 2.0)
        g6.insert_edge(2, 5, 6.0)

        (score, res) = tsp_dfs(g6)
        self.assertEqual(score, math.inf)
        self.assertEqual(res, [])

    # --- Functions for Eulerian Paths ----------------------
    def test_check_eulerian_cycle(self):
        """Test the is_eulerian_cycle() check."""
        self.assertEqual(is_eulerian_cycle(self.g1, []), False)
        self.assertEqual(is_eulerian_cycle(self.g1, [0]), True)

        g1 = Graph(1, undirected=False)
        g1.insert_edge(0, 0, 1.0)

        self.assertEqual(is_eulerian_cycle(g1, []), False)
        self.assertEqual(is_eulerian_cycle(g1, [0]), False)
        self.assertEqual(is_eulerian_cycle(g1, [0, 0]), True)

        self.assertEqual(is_eulerian_cycle(self.g2, []), False)
        self.assertEqual(is_eulerian_cycle(self.g2, [0]), False)
        self.assertEqual(is_eulerian_cycle(self.g2, [0, 1]), False)
        self.assertEqual(is_eulerian_cycle(self.g2, [1, 0]), False)
        self.assertEqual(is_eulerian_cycle(self.g2, [1, 0, 1]), False)

        self.assertEqual(is_eulerian_cycle(self.g3, []), False)
        self.assertEqual(is_eulerian_cycle(self.g3, [0]), False)
        self.assertEqual(is_eulerian_cycle(self.g3, [0, 1, 2]), False)
        self.assertEqual(is_eulerian_cycle(self.g3, [2, 0, 1, 2]), True)
        self.assertEqual(is_eulerian_cycle(self.g3, [2, 0, 1]), False)
        self.assertEqual(is_eulerian_cycle(self.g3, [2, 0, 1, 1, 2]), False)
        self.assertEqual(is_eulerian_cycle(self.g3, [2, 0, 1, 2]), True)

        self.assertEqual(is_eulerian_cycle(self.g4, []), False)
        self.assertEqual(is_eulerian_cycle(self.g4, [0]), False)
        self.assertEqual(is_eulerian_cycle(self.g4, [0, 1, 3, 2]), False)
        self.assertEqual(is_eulerian_cycle(self.g4, [0, 1, 3, 2, 0, 2, 3, 1, 0]), True)
        self.assertEqual(is_eulerian_cycle(self.g4, [1, 0, 2, 3, 1, 3, 2, 0, 1]), True)

        self.assertEqual(is_eulerian_cycle(self.g5, [0]), False)
        self.assertEqual(is_eulerian_cycle(self.g5, [0, 1, 2]), False)
        self.assertEqual(is_eulerian_cycle(self.g5, [0, 1, 0, 2, 3, 1, 3, 4]), False)
        self.assertEqual(is_eulerian_cycle(self.g5, [0, 1, 0, 2, 3, 1, 3, 4, 1]), False)
        self.assertEqual(is_eulerian_cycle(self.g5, [0, 1, 0, 2, 3, 1, 3, 4, 1, 0]), False)

    def test_has_eulerian_cycle_3(self):
        """Test has_eulerian_cycle()."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        g.insert_edge(1, 2, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        g.insert_edge(2, 0, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

        # Self loop
        g.insert_edge(1, 1, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

    def test_has_eulerian_cycle_4(self):
        """Test has_eulerian_cycle()."""
        g = Graph(4, undirected=True)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)

        # Figure 18-9
        self.assertFalse(has_eulerian_cycle(g))

        g.insert_edge(0, 3, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        g.insert_edge(2, 3, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        g.remove_edge(1, 3)
        self.assertTrue(has_eulerian_cycle(g))

    def test_has_eulerian_cycle_5(self):
        """Test has_eulerian_cycle()."""
        # Multiple singletons
        g = Graph(5, undirected=True)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        # Fully connected
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(3, 4, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

        # Add a self-loop.
        g.insert_edge(0, 0, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

    def test_has_eulerian_cycle_6b(self):
        """Test has_eulerian_cycle()."""
        # Make graph out of two disjoint components
        # where all nodes have even degree.
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(5, 3, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        # Connect the components, but make nodes odd degree.
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        # Make valid.
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(1, 4, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

    def test_has_eulerian_cycle_6(self):
        """Test has_eulerian_cycle()."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)
        self.assertFalse(has_eulerian_cycle(g))

        path = hierholzers(g)
        self.assertIsNone(path)

        g.insert_edge(3, 5, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

        # Add self loop
        g.insert_edge(4, 4, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

        # Add second self loop
        g.insert_edge(2, 2, 1.0)
        self.assertTrue(has_eulerian_cycle(g))

    def test_hierholzers_3(self):
        """Test Hierholzer's algorithm."""
        path = hierholzers(self.g3)
        self.assertTrue(is_eulerian_cycle(self.g3, path))

    def test_hierholzers_4(self):
        """Test Hierholzer's algorithm."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)

        path = hierholzers(g)
        self.assertEqual(path, [0, 1, 2, 3, 0])
        self.assertTrue(is_eulerian_cycle(g, path))

        # Insert self-loop
        g.insert_edge(2, 2, 1.0)

        path = hierholzers(g)
        self.assertEqual(path, [0, 1, 2, 2, 3, 0])
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_6(self):
        """Test Hierholzer's algorithm."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)

        path = hierholzers(g)
        self.assertIsNone(path)

        g.insert_edge(3, 5, 1.0)

        # Graph from 18-8
        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_6b(self):
        """Test Hierholzer's algorithm."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 3, 1.0)  # Different edge order
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 5, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(3, 5, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_7a(self):
        """Test Hierholzer's algorithm."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        # subloop
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 1, 1.0)

        # subsubloop
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(6, 4, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_7b(self):
        """Test Hierholzer's algorithm."""
        g = Graph(7, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        # subloop 1
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 1, 1.0)

        # subloop 2
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(6, 2, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_8a(self):
        """Test Hierholzer's algorithm."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 6, 1.0)
        g.insert_edge(3, 7, 1.0)
        g.insert_edge(4, 7, 1.0)
        g.insert_edge(5, 7, 1.0)

        path = hierholzers(g)
        self.assertIsNone(path)

        g.insert_edge(6, 7, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_8b(self):
        """Test Hierholzer's algorithm."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(3, 5, 1.0)
        g.insert_edge(3, 6, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 7, 1.0)
        g.insert_edge(4, 7, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))

    def test_hierholzers_5(self):
        """Test Hierholzer's algorithm."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 4, 1.0)

        path = hierholzers(g)
        self.assertTrue(is_eulerian_cycle(g, path))


if __name__ == "__main__":
    unittest.main()
