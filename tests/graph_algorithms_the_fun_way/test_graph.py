from graph_algorithms_the_fun_way.graph import *

import unittest


class TestGraph(unittest.TestCase):
    def test_empty(self):
        """Test we can create an empty graph."""
        g = Graph(0)
        self.assertTrue(g.is_valid())
        self.assertEqual(0, g.num_nodes)
        self.assertEqual(0, len(g.nodes))
        self.assertTrue(g.is_unlabeled())

    def test_no_edges(self):
        """Test we can create a graph with nodes but no edges."""
        g = Graph(10)
        self.assertTrue(g.is_valid())
        self.assertEqual(10, g.num_nodes)
        self.assertEqual(10, len(g.nodes))
        self.assertTrue(g.is_unlabeled())

        for i in range(10):
            self.assertEqual(i, g.nodes[i].index)
            self.assertTrue(g.nodes[i].label is None)
            self.assertEqual(0, len(g.nodes[i].edges))

    def test_insert_undirected_edge(self):
        """Test we can insert undirected edges into a graph."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertTrue(g.is_valid())

        # Check that the correct edges are there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 0))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 1))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 2))
        self.assertTrue(g.is_edge(0, 3))
        self.assertTrue(g.is_edge(3, 0))
        self.assertTrue(g.is_edge(1, 3))
        self.assertTrue(g.is_edge(3, 1))

        # Check that there are no incorrect edges.
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))

        # Check the we get an error if we insert an invalid edge.
        with self.assertRaises(IndexError):
            g.insert_edge(4, 1, 1.0)
        with self.assertRaises(IndexError):
            g.insert_edge(3, -1, 1.0)

        # Check the we get an error if we try to remove an invalid edge.
        with self.assertRaises(IndexError):
            g.remove_edge(4, 1)
        with self.assertRaises(IndexError):
            g.remove_edge(3, -1)

    def test_insert_directed_edge(self):
        """Test we can insert directed edges into a graph."""
        g = Graph(4)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertTrue(g.is_valid())

        # Check that the correct edges are there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 0))
        self.assertTrue(g.is_edge(3, 1))

        # Check that there are no incorrect edges.
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))
        self.assertFalse(g.is_edge(1, 0))
        self.assertFalse(g.is_edge(2, 1))
        self.assertFalse(g.is_edge(3, 2))
        self.assertFalse(g.is_edge(0, 3))
        self.assertFalse(g.is_edge(1, 3))

    def test_insert_weighted_edge(self):
        """Test we can insert weighted edges into a graph."""
        g = Graph(4)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(1, 2, 2.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.5)
        g.insert_edge(3, 1, -1.0)
        self.assertTrue(g.is_valid())

        # Check that the correct edges are there.
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 0.5)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 2.0)
        self.assertAlmostEqual(g.get_edge(2, 3).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(3, 0).weight, 1.5)
        self.assertAlmostEqual(g.get_edge(3, 1).weight, -1.0)

        # Check that there are no incorrect edges.
        self.assertIsNone(g.get_edge(0, 2))
        self.assertIsNone(g.get_edge(2, 0))
        self.assertIsNone(g.get_edge(1, 0))
        self.assertIsNone(g.get_edge(2, 1))
        self.assertIsNone(g.get_edge(3, 2))
        self.assertIsNone(g.get_edge(0, 3))
        self.assertIsNone(g.get_edge(1, 3))

    def test_remove_directed_edges(self):
        """Test we can remove directed edges from a graph."""
        g = Graph(4)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(1, 2, 2.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.5)
        g.insert_edge(3, 1, -1.0)
        self.assertTrue(g.is_valid())

        # Check that the correct edges are there.
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 0.5)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 2.0)
        self.assertAlmostEqual(g.get_edge(2, 3).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(3, 0).weight, 1.5)
        self.assertAlmostEqual(g.get_edge(3, 1).weight, -1.0)

        g.remove_edge(0, 1)
        self.assertIsNone(g.get_edge(0, 1))
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 2.0)
        self.assertAlmostEqual(g.get_edge(2, 3).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(3, 0).weight, 1.5)
        self.assertAlmostEqual(g.get_edge(3, 1).weight, -1.0)

        g.remove_edge(3, 1)
        self.assertIsNone(g.get_edge(0, 1))
        self.assertIsNone(g.get_edge(3, 1))
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 2.0)
        self.assertAlmostEqual(g.get_edge(2, 3).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(3, 0).weight, 1.5)

    def test_remove_undirected_edges(self):
        """Test we can remove undirected edges from a graph."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertTrue(g.is_valid())

        # Check that the correct edges are there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 0))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 1))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 2))
        self.assertTrue(g.is_edge(0, 3))
        self.assertTrue(g.is_edge(3, 0))
        self.assertTrue(g.is_edge(1, 3))
        self.assertTrue(g.is_edge(3, 1))
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))

        g.remove_edge(1, 2)
        self.assertFalse(g.is_edge(1, 2))
        self.assertFalse(g.is_edge(2, 1))

        g.remove_edge(0, 3)
        self.assertFalse(g.is_edge(3, 0))
        self.assertFalse(g.is_edge(0, 3))

        # Check that the rest of the edges are still there.
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 0))
        self.assertTrue(g.is_edge(2, 3))
        self.assertTrue(g.is_edge(3, 2))
        self.assertTrue(g.is_edge(1, 3))
        self.assertTrue(g.is_edge(3, 1))

    def test_labeling(self):
        """Test Graph's labeling functions."""
        g = Graph(4)
        self.assertTrue(g.is_unlabeled())

        g.label_node(2, 8)
        self.assertEqual(8, g.nodes[2].label)
        self.assertFalse(g.is_unlabeled())

        g.reset_labels()
        self.assertTrue(g.is_unlabeled())

    def test_is_same_structure(self):
        """Test the is_same_structure testing function."""
        g1 = Graph(3, undirected=True)
        g2 = Graph(3, undirected=True)
        self.assertTrue(g1.is_same_structure(g2))

        g1.insert_edge(0, 1, 0.1)
        self.assertFalse(g1.is_same_structure(g2))

        g2.insert_edge(0, 1, 0.2)
        self.assertFalse(g1.is_same_structure(g2))

        g2.insert_edge(0, 1, 0.1)
        self.assertTrue(g1.is_same_structure(g2))

        g1.insert_edge(2, 0, 1.0)
        g1.insert_edge(2, 1, 2.0)
        g2.insert_edge(2, 1, 2.0)
        g2.insert_edge(0, 2, 1.0)
        self.assertTrue(g1.is_same_structure(g2))

    def test_directed_make_copy(self):
        """Test that we can make a copy of the graph."""
        g = Graph(4)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(1, 2, 2.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.5)
        g.insert_edge(3, 1, -1.0)
        self.assertTrue(g.is_valid())

        g2 = g.make_copy()
        self.assertTrue(g.is_same_structure(g2))
        self.assertTrue(g2.is_same_structure(g))

        # Check that the correct edges are there.
        self.assertAlmostEqual(g2.get_edge(0, 1).weight, 0.5)
        self.assertAlmostEqual(g2.get_edge(1, 2).weight, 2.0)
        self.assertAlmostEqual(g2.get_edge(2, 3).weight, 1.0)
        self.assertAlmostEqual(g2.get_edge(3, 0).weight, 1.5)
        self.assertAlmostEqual(g2.get_edge(3, 1).weight, -1.0)

        self.assertIsNone(g2.get_edge(1, 0))
        self.assertIsNone(g2.get_edge(2, 1))
        self.assertIsNone(g2.get_edge(3, 2))
        self.assertIsNone(g2.get_edge(0, 3))
        self.assertIsNone(g2.get_edge(1, 3))
        self.assertIsNone(g2.get_edge(2, 0))
        self.assertIsNone(g2.get_edge(0, 2))

    def test_undirected_make_copy(self):
        """Test that we can make a copy of an undirected graph."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertTrue(g.is_valid())

        g2 = g.make_copy()
        self.assertTrue(g.is_same_structure(g2))
        self.assertTrue(g2.is_same_structure(g))

        # Check that the correct edges are there.
        self.assertTrue(g2.is_edge(0, 1))
        self.assertTrue(g2.is_edge(1, 0))
        self.assertTrue(g2.is_edge(1, 2))
        self.assertTrue(g2.is_edge(2, 1))
        self.assertTrue(g2.is_edge(2, 3))
        self.assertTrue(g2.is_edge(3, 2))
        self.assertTrue(g2.is_edge(0, 3))
        self.assertTrue(g2.is_edge(3, 0))
        self.assertTrue(g2.is_edge(1, 3))
        self.assertTrue(g2.is_edge(3, 1))
        self.assertFalse(g2.is_edge(0, 2))
        self.assertFalse(g2.is_edge(2, 0))

        # Make sure we don't double add the edges.
        self.assertEqual(len(g2.nodes[0].edges), 2)
        self.assertEqual(len(g2.nodes[1].edges), 3)
        self.assertEqual(len(g2.nodes[2].edges), 2)
        self.assertEqual(len(g2.nodes[3].edges), 3)

    def test_add_node(self):
        """Test that we can add new nodes to a Graph."""
        g = Graph(4, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 0, 1.0)
        self.assertTrue(g.is_valid())

        g.insert_node()
        self.assertTrue(g.is_valid())
        self.assertEqual(g.num_nodes, 5)

    def test_make_transpose(self):
        """Test that we correctly transpose a directed Graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(2, 1, 1.0)
        self.assertTrue(g.is_edge(0, 1))
        self.assertFalse(g.is_edge(1, 0))
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))
        self.assertFalse(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 1))

        gT = make_transpose_graph(g)
        self.assertFalse(gT.is_edge(0, 1))
        self.assertTrue(gT.is_edge(1, 0))
        self.assertFalse(gT.is_edge(0, 2))
        self.assertFalse(gT.is_edge(2, 0))
        self.assertTrue(gT.is_edge(1, 2))
        self.assertFalse(gT.is_edge(2, 1))

    def test_make_transpose_undirected(self):
        """Test that we correctly transpose an undirected Graph."""
        g = Graph(3, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(2, 1, 1.0)
        self.assertTrue(g.is_edge(0, 1))
        self.assertTrue(g.is_edge(1, 0))
        self.assertFalse(g.is_edge(0, 2))
        self.assertFalse(g.is_edge(2, 0))
        self.assertTrue(g.is_edge(1, 2))
        self.assertTrue(g.is_edge(2, 1))

        gT = make_transpose_graph(g)
        self.assertTrue(gT.is_edge(0, 1))
        self.assertTrue(gT.is_edge(1, 0))
        self.assertFalse(gT.is_edge(0, 2))
        self.assertFalse(gT.is_edge(2, 0))
        self.assertTrue(gT.is_edge(1, 2))
        self.assertTrue(gT.is_edge(2, 1))

    def test_get_neighbors(self):
        """Test that we correctly get the neighbors of a node."""
        # Test with a full connected, undirected graph.
        g3_full = Graph(3, undirected=True)
        g3_full.insert_edge(0, 1, 1.0)
        g3_full.insert_edge(1, 2, 1.0)
        g3_full.insert_edge(2, 0, 1.0)

        n3_full = g3_full.nodes[0].get_out_neighbors()
        self.assertFalse(0 in n3_full)
        self.assertTrue(1 in n3_full)
        self.assertTrue(2 in n3_full)

        # Test with a partially connected, directed graph.
        g4 = Graph(4, undirected=False)
        g4.insert_edge(0, 1, 1.0)
        g4.insert_edge(1, 2, 1.0)
        g4.insert_edge(2, 0, 1.0)
        g4.insert_edge(2, 1, 1.0)

        n4_0 = g4.nodes[0].get_out_neighbors()
        self.assertFalse(0 in n4_0)
        self.assertTrue(1 in n4_0)
        self.assertFalse(2 in n4_0)
        self.assertFalse(3 in n4_0)

        n4_1 = g4.nodes[1].get_out_neighbors()
        self.assertFalse(0 in n4_1)
        self.assertFalse(1 in n4_1)
        self.assertTrue(2 in n4_1)
        self.assertFalse(3 in n4_1)

        n4_2 = g4.nodes[2].get_out_neighbors()
        self.assertTrue(0 in n4_2)
        self.assertTrue(1 in n4_2)
        self.assertFalse(2 in n4_2)
        self.assertFalse(3 in n4_2)

        n4_3 = g4.nodes[3].get_out_neighbors()
        self.assertFalse(0 in n4_3)
        self.assertFalse(1 in n4_3)
        self.assertFalse(2 in n4_3)
        self.assertFalse(3 in n4_2)

    def test_get_neighbors_Figure_2_1(self):
        """Test that we correctly get the neighbors of the node in Figure 2.1"""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 5, 1.0)
        self.assertEqual(set(g.nodes[0].get_neighbors()), set([1, 3, 4]))
        self.assertEqual(set(g.nodes[1].get_neighbors()), set([0, 2, 4]))
        self.assertEqual(set(g.nodes[2].get_neighbors()), set([1, 4, 5]))
        self.assertEqual(set(g.nodes[3].get_neighbors()), set([0]))
        self.assertEqual(set(g.nodes[4].get_neighbors()), set([0, 1, 2, 5]))
        self.assertEqual(set(g.nodes[5].get_neighbors()), set([2, 4]))

    def test_in_neighbors(self):
        """Test that we can correctly compute a node's in-neighbors."""
        g4 = Graph(4, undirected=False)
        g4.insert_edge(0, 1, 1.0)
        g4.insert_edge(1, 2, 1.0)
        g4.insert_edge(2, 0, 1.0)
        g4.insert_edge(2, 1, 1.0)

        n4_0 = g4.get_in_neighbors(0)
        self.assertFalse(0 in n4_0)
        self.assertFalse(1 in n4_0)
        self.assertTrue(2 in n4_0)
        self.assertFalse(3 in n4_0)

        n4_1 = g4.get_in_neighbors(1)
        self.assertTrue(0 in n4_1)
        self.assertFalse(1 in n4_1)
        self.assertTrue(2 in n4_1)
        self.assertFalse(3 in n4_1)

        n4_2 = g4.get_in_neighbors(2)
        self.assertFalse(0 in n4_2)
        self.assertTrue(1 in n4_2)
        self.assertFalse(2 in n4_2)
        self.assertFalse(3 in n4_2)

        n4_3 = g4.get_in_neighbors(3)
        self.assertFalse(0 in n4_3)
        self.assertFalse(1 in n4_3)
        self.assertFalse(2 in n4_3)
        self.assertFalse(3 in n4_2)

        # Test that an undirect graph produces useful results.
        g3_full = Graph(3, undirected=True)
        g3_full.insert_edge(0, 1, 1.0)
        g3_full.insert_edge(1, 2, 1.0)
        g3_full.insert_edge(2, 0, 1.0)

        n3_full = g3_full.get_in_neighbors(0)
        self.assertFalse(0 in n3_full)
        self.assertTrue(1 in n3_full)
        self.assertTrue(2 in n3_full)

    def test_in_neighbors_5(self):
        """Test that we can correctly compute a node's in-neighbors with a 5 node graph."""
        g5 = Graph(5, undirected=False)
        g5.insert_edge(0, 1, 1.0)
        g5.insert_edge(0, 3, 1.0)
        g5.insert_edge(0, 4, 1.0)
        g5.insert_edge(1, 1, 1.0)
        g5.insert_edge(1, 2, 1.0)
        g5.insert_edge(1, 3, 1.0)
        g5.insert_edge(2, 0, 1.0)
        g5.insert_edge(2, 1, 1.0)
        g5.insert_edge(3, 2, 1.0)
        g5.insert_edge(3, 3, 1.0)
        g5.insert_edge(3, 4, 1.0)
        g5.insert_edge(4, 3, 1.0)
        g5.insert_edge(4, 0, 1.0)

        n5_0 = g5.get_in_neighbors(0)
        self.assertFalse(0 in n5_0)
        self.assertFalse(1 in n5_0)
        self.assertTrue(2 in n5_0)
        self.assertFalse(3 in n5_0)
        self.assertTrue(4 in n5_0)

        n5_1 = g5.get_in_neighbors(1)
        self.assertTrue(0 in n5_1)
        self.assertTrue(1 in n5_1)
        self.assertTrue(2 in n5_1)
        self.assertFalse(3 in n5_1)
        self.assertFalse(4 in n5_1)

        n5_2 = g5.get_in_neighbors(2)
        self.assertFalse(0 in n5_2)
        self.assertTrue(1 in n5_2)
        self.assertFalse(2 in n5_2)
        self.assertTrue(3 in n5_2)
        self.assertFalse(4 in n5_2)

        n5_3 = g5.get_in_neighbors(3)
        self.assertTrue(0 in n5_3)
        self.assertTrue(1 in n5_3)
        self.assertFalse(2 in n5_3)
        self.assertTrue(3 in n5_3)
        self.assertTrue(4 in n5_3)

        n5_4 = g5.get_in_neighbors(4)
        self.assertTrue(0 in n5_4)
        self.assertFalse(1 in n5_4)
        self.assertFalse(2 in n5_4)
        self.assertTrue(3 in n5_4)
        self.assertFalse(4 in n5_4)

    def test_undirected_degree_Figure_2_3(self):
        """Test that we can correctly compute nodes' degrees in Figure 2.3"""
        g = Graph(6, undirected=True)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(0, 4, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 4, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 5, 1.0)
        self.assertEqual(g.nodes[0].undirected_degree(), 3)
        self.assertEqual(g.nodes[1].undirected_degree(), 3)
        self.assertEqual(g.nodes[2].undirected_degree(), 3)
        self.assertEqual(g.nodes[3].undirected_degree(), 1)
        self.assertEqual(g.nodes[4].undirected_degree(), 4)
        self.assertEqual(g.nodes[5].undirected_degree(), 2)

        # Test that we correctly handle self-loops
        g.insert_edge(2, 2, 1.0)
        self.assertEqual(g.nodes[2].undirected_degree(), 5)

    def test_in_out_degree_Figure_2_4(self):
        """Test that we can correctly compute nodes' degrees in Figure 2.4"""
        g = Graph(6, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 3, 1.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(1, 4, 1.0)
        g.insert_edge(2, 2, 1.0)
        g.insert_edge(2, 5, 1.0)
        g.insert_edge(4, 0, 1.0)
        g.insert_edge(4, 2, 1.0)
        g.insert_edge(5, 2, 1.0)
        g.insert_edge(5, 4, 1.0)
        self.assertEqual(g.nodes[0].out_degree(), 2)
        self.assertEqual(g.nodes[1].out_degree(), 2)
        self.assertEqual(g.nodes[2].out_degree(), 2)
        self.assertEqual(g.nodes[3].out_degree(), 0)
        self.assertEqual(g.nodes[4].out_degree(), 2)
        self.assertEqual(g.nodes[5].out_degree(), 2)

        self.assertEqual(len(g.get_in_neighbors(0)), 1)
        self.assertEqual(len(g.get_in_neighbors(1)), 1)
        self.assertEqual(len(g.get_in_neighbors(2)), 4)
        self.assertEqual(len(g.get_in_neighbors(3)), 1)
        self.assertEqual(len(g.get_in_neighbors(4)), 2)
        self.assertEqual(len(g.get_in_neighbors(5)), 1)

    def test_make_neighborhood_subgraph(self):
        """Test that we can make a subgraph from a node's neighborhood."""
        g7 = Graph(7, undirected=True)
        g7.insert_edge(0, 1, 1.0)
        g7.insert_edge(0, 4, 1.0)
        g7.insert_edge(1, 2, 1.0)
        g7.insert_edge(1, 5, 1.0)
        g7.insert_edge(1, 6, 1.0)
        g7.insert_edge(2, 3, 1.0)
        g7.insert_edge(3, 6, 1.0)
        g7.insert_edge(5, 6, 1.0)

        # Closed neighborhood
        g_sub = g7.make_undirected_neighborhood_subgraph(1, True)
        self.assertEqual(g_sub.num_nodes, 5)

        expected_edges = set([(0, 1), (1, 2), (1, 3), (1, 4), (3, 4)])
        for u in range(4):
            for v in range(u + 1, 5):
                self.assertEqual(g_sub.is_edge(u, v), (u, v) in expected_edges)

        # Open neighborhood
        g_sub = g7.make_undirected_neighborhood_subgraph(1, False)
        self.assertEqual(g_sub.num_nodes, 4)

        expected_edges = set([(2, 3)])
        for u in range(3):
            for v in range(u + 1, 4):
                self.assertEqual(g_sub.is_edge(u, v), (u, v) in expected_edges)

        # Small graph
        g3 = Graph(3, undirected=True)
        g3.insert_edge(0, 1, 1.0)
        g3_sub = g3.make_undirected_neighborhood_subgraph(1, True)
        self.assertEqual(g3_sub.num_nodes, 2)
        self.assertTrue(g3_sub.is_edge(0, 1))
        self.assertFalse(g3_sub.is_edge(0, 0))

        # Try a directed graph
        g5 = Graph(5, undirected=False)
        g5.insert_edge(0, 1, 1.0)
        g5.insert_edge(0, 3, 1.0)
        g5.insert_edge(1, 2, 1.0)
        g5.insert_edge(2, 4, 1.0)
        g5.insert_edge(4, 1, 1.0)

        with self.assertRaises(ValueError):
            g_sub = g5.make_undirected_neighborhood_subgraph(1, True)

    def test_make_graph_from_edges(self):
        """Test that we can construct a graph from a list of edges."""
        edge_list = [Edge(0, 1, 1.0), Edge(1, 3, 10.0), Edge(2, 4, 5.0), Edge(3, 1, 2.0), Edge(1, 2, 3.0)]
        g = make_graph_from_edges(5, False, edge_list)
        self.assertEqual(g.num_nodes, 5)

        edges = [(0, 1), (1, 3), (2, 4), (3, 1), (1, 2)]
        for i in range(5):
            for j in range(5):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                else:
                    self.assertFalse(g.is_edge(i, j))

        self.assertAlmostEqual(g.get_edge(0, 1).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 3).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(2, 4).weight, 5.0)
        self.assertAlmostEqual(g.get_edge(3, 1).weight, 2.0)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 3.0)


if __name__ == "__main__":
    unittest.main()
