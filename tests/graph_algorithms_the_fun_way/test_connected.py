import unittest

from graph_algorithms_the_fun_way.connected import *
from graph_algorithms_the_fun_way.graph import Graph, edge_in_list


class TestGraphConnected(unittest.TestCase):
    def setUp(self):
        """Set up a graph used in a few tests."""
        self.g6 = Graph(6, undirected=False)
        self.g6.insert_edge(0, 2, 1.0)
        self.g6.insert_edge(2, 3, 1.0)
        self.g6.insert_edge(3, 0, 1.0)
        self.g6.insert_edge(3, 5, 1.0)
        self.g6.insert_edge(5, 4, 1.0)
        self.g6.insert_edge(4, 5, 1.0)

    def test_get_reachable_all(self):
        """Test get_reachable."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(0, 2, 1.0)

        reachable = get_reachable(g, 0)
        self.assertTrue(0 in reachable)
        self.assertTrue(1 in reachable)
        self.assertTrue(2 in reachable)

    def test_get_reachable_some(self):
        """Test get_reachable."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(1, 2, 1.0)

        reachable = get_reachable(g, 0)
        self.assertTrue(0 in reachable)
        self.assertTrue(1 in reachable)
        self.assertTrue(2 in reachable)

        reachable = get_reachable(g, 1)
        self.assertTrue(0 in reachable)
        self.assertTrue(1 in reachable)
        self.assertTrue(2 in reachable)

        reachable = get_reachable(g, 2)
        self.assertFalse(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertTrue(2 in reachable)

    def test_get_reachable_6(self):
        """Test get_reachable."""
        # Everything is reachable from 0 except 1.
        reachable = get_reachable(self.g6, 0)
        self.assertTrue(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertTrue(2 in reachable)
        self.assertTrue(3 in reachable)
        self.assertTrue(4 in reachable)
        self.assertTrue(5 in reachable)

        # 1 can only reach itself.
        reachable = get_reachable(self.g6, 1)
        for i in range(6):
            self.assertEqual(i in reachable, i == 1)

        # Everything is reachable from 2 except 1.
        reachable = get_reachable(self.g6, 2)
        self.assertTrue(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertTrue(2 in reachable)
        self.assertTrue(3 in reachable)
        self.assertTrue(4 in reachable)
        self.assertTrue(5 in reachable)

        # Everything is reachable from 3 except 1.
        reachable = get_reachable(self.g6, 3)
        self.assertTrue(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertTrue(2 in reachable)
        self.assertTrue(3 in reachable)
        self.assertTrue(4 in reachable)
        self.assertTrue(5 in reachable)

        # Onle 4 and 5 are reachable from 4
        reachable = get_reachable(self.g6, 4)
        self.assertFalse(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertFalse(2 in reachable)
        self.assertFalse(3 in reachable)
        self.assertTrue(4 in reachable)
        self.assertTrue(5 in reachable)

        # Onle 4 and 5 are reachable from 5
        reachable = get_reachable(self.g6, 5)
        self.assertFalse(0 in reachable)
        self.assertFalse(1 in reachable)
        self.assertFalse(2 in reachable)
        self.assertFalse(3 in reachable)
        self.assertTrue(4 in reachable)
        self.assertTrue(5 in reachable)

    def test_check_strongly_connected_reachable_6(self):
        """Test check_strongly_connected."""
        self.assertTrue(check_strongly_connected(self.g6, [1]))
        self.assertTrue(check_strongly_connected(self.g6, [0]))
        self.assertTrue(check_strongly_connected(self.g6, [0, 2, 3]))
        self.assertTrue(check_strongly_connected(self.g6, [4, 5]))
        self.assertTrue(check_strongly_connected(self.g6, [1]))
        self.assertFalse(check_strongly_connected(self.g6, [0, 1]))
        self.assertFalse(check_strongly_connected(self.g6, [0, 2, 3, 4]))
        self.assertFalse(check_strongly_connected(self.g6, [4, 5, 0]))
        self.assertFalse(check_strongly_connected(self.g6, [1, 2]))
        self.assertFalse(check_strongly_connected(self.g6, [0, 1, 2, 3]))

    def test_scc_figure_12_1(self):
        """Test the Kosaraju-Sharir algorithm on the graph from Figure 12-1"""
        g = Graph(6, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(4, 3, 1.0)
        g.insert_edge(4, 5, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 3)
        self.assertEqual(set(components[0]), set([0, 1, 3, 4]))
        self.assertEqual(set(components[1]), set([2]))
        self.assertEqual(set(components[2]), set([5]))

    def test_scc_figure_12_3(self):
        """Test the Kosaraju-Sharir algorithm on the graph from Figure 12-3"""
        g = Graph(6, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(4, 0, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 3, 1.0)
        g.insert_edge(5, 2, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(5, 4, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 2)
        self.assertEqual(set(components[1]), set([0, 1, 3, 4]))
        self.assertEqual(set(components[0]), set([2, 5]))

    def test_scc_figure_12_5(self):
        """Test the Kosaraju-Sharir algorithm on the graph from Figure 12-5"""
        g = Graph(6, undirected=False)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 5, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(5, 4, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 3)
        self.assertEqual(set(components[0]), set([1]))
        self.assertEqual(set(components[1]), set([0, 2, 3]))
        self.assertEqual(set(components[2]), set([4, 5]))

    def test_kosaraju_3a(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(0, 2, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 1)
        self.assertEqual(set(components[0]), set([0, 1, 2]))
        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_3b(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(1, 2, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 2)
        self.assertEqual(set(components[1]), set([2]))
        self.assertEqual(set(components[0]), set([0, 1]))

        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_3c(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 1)
        self.assertEqual(set(components[0]), set([0, 1, 2]))
        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_3d(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(2, 1, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 2)
        self.assertEqual(set(components[1]), set([0, 1]))
        self.assertEqual(components[0], [2])

    def test_kosaraju_4a(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 3)
        self.assertEqual(set(components[0]), set([3]))
        self.assertEqual(set(components[1]), set([2]))
        self.assertEqual(set(components[2]), set([0, 1]))
        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_4b(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 0, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 2)
        self.assertEqual(set(components[0]), set([3]))
        self.assertEqual(set(components[1]), set([0, 1, 2]))
        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_5(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 1, 1.0)

        components = kosaraju_sharir(g)
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 5)
        for c in components:
            self.assertTrue(check_strongly_connected(g, c))

    def test_kosaraju_6(self):
        """Test the Kosaraju-Sharir algorithm on an example graph."""
        components = kosaraju_sharir(self.g6)
        self.assertEqual(len(components), 3)
        self.assertEqual(set(components[1]), set([0, 2, 3]))
        self.assertEqual(set(components[2]), set([4, 5]))
        self.assertEqual(set(components[0]), set([1]))
        for c in components:
            self.assertTrue(check_strongly_connected(self.g6, c))

    def test_bridge_1(self):
        """Test the bridge finding algorithm on an example graph."""
        g = Graph(1, undirected=True)
        res = find_bridges(g)
        self.assertEqual(len(res), 0)

        # Self-edge is not a bridge
        g.insert_edge(0, 0, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 0)

    def test_bridge_4(self):
        """Test the bridge finding algorithm on an example graph."""
        g = Graph(4, undirected=True)

        # No edges = no bridges
        res = find_bridges(g)
        self.assertEqual(len(res), 0)

        # A line is completely breakable.
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(edge_in_list(res, 0, 1, True))
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 2, 3, True))

        # Add more edges
        g.insert_edge(0, 2, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(edge_in_list(res, 2, 3, True))

        g.insert_edge(1, 3, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 0)

    def test_bridge_5(self):
        """Test the bridge finding algorithm on an example graph."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 4, 1.0)

        # A line is completely breakable.
        res = find_bridges(g)
        self.assertEqual(len(res), 4)
        self.assertTrue(edge_in_list(res, 0, 1, True))
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 2, 3, True))
        self.assertTrue(edge_in_list(res, 3, 4, True))

        # A ring is not breakable
        g.insert_edge(4, 0, 1.0)

        res = find_bridges(g)
        self.assertEqual(len(res), 0)
        self.assertFalse(edge_in_list(res, 0, 1, True))
        self.assertFalse(edge_in_list(res, 1, 2, True))
        self.assertFalse(edge_in_list(res, 2, 3, True))
        self.assertFalse(edge_in_list(res, 3, 4, True))
        self.assertFalse(edge_in_list(res, 4, 0, True))

    def test_bridge_6(self):
        """Test the bridge finding algorithm on an example graph."""
        g = Graph(6, undirected=True)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 4, 1.0)

        res = find_bridges(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(edge_in_list(res, 0, 1, True))
        self.assertTrue(edge_in_list(res, 2, 3, True))
        self.assertTrue(edge_in_list(res, 3, 4, True))

        self.assertFalse(edge_in_list(res, 1, 4, True))
        self.assertFalse(edge_in_list(res, 2, 4, True))
        self.assertFalse(edge_in_list(res, 0, 2, True))

        # Add some more edges
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(0, 2, 1.0)

        res = find_bridges(g)
        self.assertEqual(len(res), 0)
        self.assertFalse(edge_in_list(res, 0, 1, True))
        self.assertFalse(edge_in_list(res, 2, 3, True))
        self.assertFalse(edge_in_list(res, 1, 4, True))
        self.assertFalse(edge_in_list(res, 2, 4, True))
        self.assertFalse(edge_in_list(res, 0, 2, True))
        self.assertFalse(edge_in_list(res, 3, 4, True))

    def test_bridge_6b(self):
        """Test the bridge finding algorithm on an example graph."""
        g = Graph(6, undirected=True)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)
        g.insert_edge(4, 5, 1.0)

        res = find_bridges(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(edge_in_list(res, 0, 1, True))
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 4, 5, True))
        self.assertFalse(edge_in_list(res, 2, 3, True))
        self.assertFalse(edge_in_list(res, 2, 4, True))
        self.assertFalse(edge_in_list(res, 3, 4, True))

        # Add an edge
        g.insert_edge(0, 4, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(edge_in_list(res, 4, 5, True))

        # Remove an edge
        g.remove_edge(1, 2)
        res = find_bridges(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(edge_in_list(res, 0, 1, True))
        self.assertTrue(edge_in_list(res, 0, 4, True))
        self.assertTrue(edge_in_list(res, 4, 5, True))

        # Add an edge
        g.insert_edge(1, 3, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(edge_in_list(res, 4, 5, True))

        # Remove an edge
        g.remove_edge(2, 4)
        res = find_bridges(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(edge_in_list(res, 4, 5, True))
        self.assertTrue(edge_in_list(res, 2, 3, True))

    def test_bridge_8(self):
        """Test the bridge finding algorithm on an example graph."""
        g: Graph = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 6, 1.0)
        g.insert_edge(3, 7, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(6, 7, 1.0)

        res = find_bridges(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 4, 5, True))
        self.assertFalse(edge_in_list(res, 1, 4, True))

        # Add some edges
        g.insert_edge(3, 6, 1.0)
        g.insert_edge(1, 5, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(edge_in_list(res, 1, 2, True))

        # Add an edge
        g.insert_edge(5, 6, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 0)

        # Remove an edge
        g.remove_edge(1, 5)
        g.remove_edge(4, 5)
        res = find_bridges(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 5, 6, True))

        # Remove an edge
        g.remove_edge(3, 7)
        res = find_bridges(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(edge_in_list(res, 1, 2, True))
        self.assertTrue(edge_in_list(res, 5, 6, True))
        self.assertTrue(edge_in_list(res, 6, 7, True))

        # Add an edge
        g.insert_edge(4, 7, 1.0)
        res = find_bridges(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(edge_in_list(res, 5, 6, True))

    def test_articulation_points_root(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 4, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(0 in res)
        self.assertTrue(2 in res)

        # Add some more edges
        g.insert_edge(1, 2, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(res, {2})

        # Add some more edges
        g.insert_edge(1, 3, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

    def test_articulation_points_1(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(1, undirected=True)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

        # Self-edge does not make an articulation point
        g.insert_edge(0, 0, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

    def test_articulation_points_5(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(5, undirected=True)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 4, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(res, {3})

        g.insert_edge(1, 4, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(1 in res)
        self.assertTrue(3 in res)
        self.assertTrue(4 in res)

        g.insert_edge(0, 2, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

        g.insert_edge(1, 3, 1.0)
        g.remove_edge(0, 2)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(1 in res)
        self.assertTrue(3 in res)

        g.insert_edge(0, 4, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(3 in res)

    def test_articulation_points_5_star(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(5, undirected=True)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(1, 4, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(1 in res)

        g.insert_edge(0, 2, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(1 in res)

        g.insert_edge(3, 4, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(1 in res)

        g.insert_edge(2, 3, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

    def test_articulation_points_6(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(1 in res)
        self.assertTrue(2 in res)

        g.insert_edge(1, 3, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 2)
        self.assertTrue(1 in res)
        self.assertTrue(2 in res)

        g.insert_edge(3, 5, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 3)
        self.assertTrue(1 in res)
        self.assertTrue(2 in res)
        self.assertTrue(3 in res)

        g.insert_edge(4, 5, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(1 in res)

        g.insert_edge(0, 4, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

        g.remove_edge(1, 2)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

        g.remove_edge(2, 4)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 1)
        self.assertTrue(3 in res)

        g.insert_edge(2, 5, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

    def test_articulation_points_8(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(8, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 6, 1.0)
        g.insert_edge(3, 7, 1.0)
        g.insert_edge(6, 7, 1.0)

        res = find_articulation_points(g)
        self.assertEqual(len(res), 3)
        expected = [1, 2, 4]
        for i in range(8):
            self.assertEqual(i in expected, i in res)

        g.insert_edge(5, 6, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

        g.remove_edge(6, 7)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 2)
        expected = [2, 3]
        for i in range(8):
            self.assertEqual(i in expected, i in res)

        g.remove_edge(3, 7)
        res = find_articulation_points(g)
        self.assertEqual(res, {2})

        g.insert_edge(1, 6, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(res, {2})

        g.insert_edge(3, 4, 1.0)
        res = find_articulation_points(g)
        self.assertEqual(len(res), 0)

    def test_articulation_points_9(self):
        """Test the bridge articulation point algorithm on an example graph."""
        g = Graph(9, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 7, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(3, 5, 1.0)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(5, 6, 1.0)
        g.insert_edge(7, 8, 1.0)

        res = find_articulation_points(g)
        expected = [0, 1, 2, 5, 7]
        self.assertEqual(len(res), len(expected))
        for i in range(9):
            self.assertEqual(i in expected, i in res)

        g.insert_edge(4, 8, 1.0)
        res = find_articulation_points(g)
        expected = [5]
        self.assertEqual(len(res), len(expected))
        for i in range(9):
            self.assertEqual(i in expected, i in res)

    def test_ap_labyrinth(self):
        """Test the labyrinth example from the book."""
        g = Graph(5, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(3, 4, 1.0)

        stats = DFSTreeStats(g.num_nodes)
        results: set = set()
        articulation_point_root(g, 0, stats, results)
        self.assertEqual(stats.parent, [-1, 0, 1, 1, 3])
        self.assertEqual(stats.order, [0, 1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
