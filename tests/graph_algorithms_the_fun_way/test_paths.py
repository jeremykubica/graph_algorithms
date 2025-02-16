import unittest

from graph_algorithms_the_fun_way.graph import Edge, Graph
from graph_algorithms_the_fun_way.paths import (
    check_edge_path_valid,
    check_last_path_valid,
    check_node_path_valid,
    compute_path_cost,
    edge_path_to_node_path,
    node_path_to_edge_path,
    make_node_path_from_last,
)


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


if __name__ == "__main__":
    unittest.main()
