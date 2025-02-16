from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from graph_algorithms_the_fun_way.file_reader import (
    make_graph_from_dependencies,
    make_graph_from_multi_csv,
    make_graph_from_weighted_csv,
    make_graph_from_weighted_csv2,
    save_graph_to_csv,
)
from graph_algorithms_the_fun_way.graph import Graph


class TestFileReaders(unittest.TestCase):

    def setUp(self):
        """Create the location of the test data directory."""
        self._test_data_dir = Path(__file__).parent / "test_data"

    def test_weighted_csv(self):
        """Test that we can read an undirected graph from a csv file."""
        g = make_graph_from_weighted_csv(self._test_data_dir / "weighted.csv", True)
        self.assertEqual(g.num_nodes, 6)

        edges = [(0, 1), (1, 0), (1, 2), (2, 1), (3, 4), (4, 3)]
        for i in range(6):
            for j in range(6):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                else:
                    self.assertFalse(g.is_edge(i, j))

        self.assertAlmostEqual(g.get_edge(0, 1).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 0).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(2, 1).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(3, 4).weight, 5.0)
        self.assertAlmostEqual(g.get_edge(4, 3).weight, 5.0)

    def test_weighted_csv2(self):
        """Test that we can read an undirected graph from a csv file."""
        g = make_graph_from_weighted_csv2(self._test_data_dir / "weighted.csv", True)
        self.assertEqual(g.num_nodes, 6)

        edges = [(0, 1), (1, 0), (1, 2), (2, 1), (3, 4), (4, 3)]
        for i in range(6):
            for j in range(6):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                else:
                    self.assertFalse(g.is_edge(i, j))

        self.assertAlmostEqual(g.get_edge(0, 1).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 0).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(2, 1).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(3, 4).weight, 5.0)
        self.assertAlmostEqual(g.get_edge(4, 3).weight, 5.0)

    def test_directed_csv(self):
        """Test that we can read a directed graph from a csv file."""
        g = make_graph_from_weighted_csv(self._test_data_dir / "weighted.csv", False)
        self.assertEqual(g.num_nodes, 6)

        edges = [(0, 1), (1, 2), (3, 4)]
        for i in range(6):
            for j in range(6):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                else:
                    self.assertFalse(g.is_edge(i, j))
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(3, 4).weight, 5.0)

    def test_directed_csv2(self):
        """Test that we can read a directed graph from a csv file."""
        g = make_graph_from_weighted_csv2(self._test_data_dir / "weighted.csv", False)
        self.assertEqual(g.num_nodes, 6)

        edges = [(0, 1), (1, 2), (3, 4)]
        for i in range(6):
            for j in range(6):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                else:
                    self.assertFalse(g.is_edge(i, j))
        self.assertAlmostEqual(g.get_edge(0, 1).weight, 1.0)
        self.assertAlmostEqual(g.get_edge(1, 2).weight, 10.0)
        self.assertAlmostEqual(g.get_edge(3, 4).weight, 5.0)

    def test_simple_write(self):
        """Check that we can save a graph as a csv."""
        g1 = Graph(3, undirected=False)
        g1.insert_edge(0, 1, 3.5)
        g1.insert_edge(1, 0, 2.5)

        with TemporaryDirectory() as dir_name:
            filename = f"{dir_name}/test.csv"
            save_graph_to_csv(g1, filename)

            # Test the file
            f = open(filename, "r")
            self.assertEqual(f.read(), "0\n1\n2\n0,1,3.5\n1,0,2.5\n")
            f.close()

    def test_write_then_read(self):
        """Check that we can save a graph as a csv and reload it."""
        g1 = Graph(6, undirected=False)
        g1.insert_edge(0, 1, 3.5)
        g1.insert_edge(1, 0, 2.5)
        g1.insert_edge(0, 2, 0.5)
        g1.insert_edge(2, 3, 1.0)
        g1.insert_edge(0, 3, 2.0)
        g1.insert_edge(3, 4, 1.0)
        g1.insert_edge(3, 1, 2.0)
        g1.insert_edge(4, 1, 0.5)

        with TemporaryDirectory() as dir_name:
            filename = f"{dir_name}/test.csv"
            save_graph_to_csv(g1, filename)

            g2 = make_graph_from_weighted_csv(filename, False)
            self.assertEqual(g1.num_nodes, g2.num_nodes)
            self.assertTrue(g1.is_same_structure(g2))

    def test_multi_csv(self):
        """Test that we can load a graph from a co-occurrence file."""
        g = make_graph_from_multi_csv("./test_data/multi.csv")
        self.assertEqual(g.num_nodes, 8)

        edges = [
            (0, 1),
            (1, 0),
            (0, 2),
            (2, 0),
            (1, 2),
            (2, 1),
            (3, 4),
            (4, 3),
            (0, 3),
            (3, 0),
            (5, 2),
            (2, 5),
            (6, 2),
            (2, 6),
            (7, 2),
            (2, 7),
            (5, 6),
            (6, 5),
            (5, 7),
            (7, 5),
            (6, 7),
            (7, 6),
            (2, 4),
            (4, 2),
        ]
        for i in range(8):
            for j in range(8):
                if (i, j) in edges:
                    self.assertTrue(g.is_edge(i, j))
                    if i + j == 1:
                        self.assertEqual(g.get_edge(i, j).weight, 2.0)
                    else:
                        self.assertEqual(g.get_edge(i, j).weight, 1.0)
                else:
                    self.assertFalse(g.is_edge(i, j))

    def test_dependencies(self):
        """Test that we can construct a graph from given dependencies."""
        priors = {0: [], 1: [0], 2: [0, 1], 3: [], 4: [1, 3], 5: [2, 4]}
        g = make_graph_from_dependencies(priors)
        self.assertEqual(g.num_nodes, 6)

        edges = [(0, 1), (0, 2), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5)]
        for i in range(6):
            for j in range(6):
                self.assertEqual((i, j) in edges, g.is_edge(i, j))


if __name__ == "__main__":
    unittest.main()
