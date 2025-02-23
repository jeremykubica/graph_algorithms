import unittest

from graph_algorithms_the_fun_way.graph import Graph
from graph_algorithms_the_fun_way.shortest_path import *


class TestShortestPath(unittest.TestCase):
    def test_dijkstras_3a(self):
        """Test Dijkstra's algorithm on a sample graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(2, 1, 0.75)

        last = Dijkstras(g, 0)
        self.assertEqual(len(last), 3)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], 0)

    def test_bellmanford_3a(self):
        """Test the Bellman-Ford algorithm on a sample graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(2, 1, 0.75)

        last = BellmanFord(g, 0)
        self.assertEqual(len(last), 3)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], 0)

    def test_dijkstras_3b(self):
        """Test Dijkstras algorithm on a sample graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(2, 1, 0.75)

        last = Dijkstras(g, 0)
        self.assertEqual(len(last), 3)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 2)
        self.assertEqual(last[2], 0)

    def test_bellmanford_3b(self):
        """Test the Bellman-Ford algorithm on a sample graph."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(2, 1, 0.75)

        last = BellmanFord(g, 0)
        self.assertEqual(len(last), 3)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 2)
        self.assertEqual(last[2], 0)

    def test_bellmanford_figure(self):
        """Test the Belmman-Ford algorithm on the graph in Figure 7-6."""
        g = Graph(3, undirected=False)
        g.insert_edge(2, 1, 1.0)
        g.insert_edge(1, 0, 1.0)
        g.insert_edge(2, 0, 10.0)

        last = BellmanFord(g, 2)
        self.assertEqual(len(last), 3)
        self.assertEqual(last[0], 1)
        self.assertEqual(last[1], 2)
        self.assertEqual(last[2], -1)

    def test_dijkstras_5(self):
        """Test Dijkstra's algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 3, 2.1)
        g.insert_edge(2, 3, 5.0)
        g.insert_edge(3, 2, 5.0)
        g.insert_edge(2, 4, 0.7)
        g.insert_edge(3, 4, 2.5)
        g.insert_edge(4, 0, 2.5)

        last = Dijkstras(g, 0)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 1)
        self.assertEqual(last[4], 2)

        last = Dijkstras(g, 1)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 4)
        self.assertEqual(last[1], -1)
        self.assertEqual(last[2], 3)
        self.assertEqual(last[3], 1)
        self.assertEqual(last[4], 3)

        last = Dijkstras(g, 2)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 4)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], -1)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], 2)

    def test_bellmanford_5(self):
        """Test the Bellman-Ford algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 3, 2.1)
        g.insert_edge(2, 3, 5.0)
        g.insert_edge(3, 2, 5.0)
        g.insert_edge(2, 4, 0.7)
        g.insert_edge(3, 4, 2.5)
        g.insert_edge(4, 0, 2.5)

        last = BellmanFord(g, 0)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 1)
        self.assertEqual(last[4], 2)

        last = BellmanFord(g, 1)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 4)
        self.assertEqual(last[1], -1)
        self.assertEqual(last[2], 3)
        self.assertEqual(last[3], 1)
        self.assertEqual(last[4], 3)

        last = BellmanFord(g, 2)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 4)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], -1)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], 2)

    def test_dijkstras_5_star(self):
        """Test Dijkstra's algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 3.5)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(0, 3, 2.0)
        g.insert_edge(1, 0, 2.5)
        g.insert_edge(1, 4, 0.5)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        g.insert_edge(3, 4, 3.0)
        g.insert_edge(4, 1, 1.0)

        last = Dijkstras(g, 0)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 3)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], 1)

        last = Dijkstras(g, 4)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 1)
        self.assertEqual(last[1], 4)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], -1)

    def test_bellmanford_5_star(self):
        """Test the Bellman-Ford algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 3.5)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(0, 3, 2.0)
        g.insert_edge(1, 0, 2.5)
        g.insert_edge(1, 4, 0.5)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        g.insert_edge(3, 4, 3.0)
        g.insert_edge(4, 1, 1.0)

        last = BellmanFord(g, 0)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 3)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], 1)

        last = BellmanFord(g, 4)
        self.assertEqual(len(last), 5)
        self.assertEqual(last[0], 1)
        self.assertEqual(last[1], 4)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 2)
        self.assertEqual(last[4], -1)

    def test_bellmanford_4_negA(self):
        """Test the Bellman-Ford algorithm on a graph with a negative edge."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 2, -0.5)
        g.insert_edge(3, 1, 3.0)

        last = BellmanFord(g, 0)
        self.assertEqual(len(last), 4)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], 0)
        self.assertEqual(last[3], 2)

    def test_bellmanford_4_negB(self):
        """Test the Bellman-Ford algorithm on a graph with a negative loop."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(2, 3, 0.5)
        g.insert_edge(3, 2, -1.0)
        g.insert_edge(3, 1, 3.0)

        last = BellmanFord(g, 0)
        self.assertEqual(last, None)

    def test_bellmanford_5_neg(self):
        """Test the Bellman-Ford algorithm on a graph with a negative loop."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 2.0)
        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 3, 0.5)
        g.insert_edge(3, 4, -10.0)
        g.insert_edge(4, 0, 3.0)

        last = BellmanFord(g, 0)
        self.assertEqual(last, None)

    def test_dijkstras_disconnected(self):
        """Test Dijkstra's algorithm on a disconnected graph."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 2, 1.0)

        last = Dijkstras(g, 0)
        self.assertEqual(len(last), 4)
        self.assertEqual(last[0], -1)
        self.assertEqual(last[1], 0)
        self.assertEqual(last[2], -1)
        self.assertEqual(last[3], -1)

    def test_floyd_warshall_4(self):
        """Test the Floyd-Warshall algorithm on the graph from Figure 7-10."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 10.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 2, 3.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)

        last = FloydWarshall(g)
        self.assertEqual(len(last), 4)
        for i in range(4):
            self.assertEqual(len(last[i]), 4)
            self.assertEqual(last[i][i], -1)

        self.assertEqual(last[0][1], 3)
        self.assertEqual(last[0][2], 0)
        self.assertEqual(last[0][3], 2)

        self.assertEqual(last[1][0], -1)
        self.assertEqual(last[1][2], 1)
        self.assertEqual(last[1][3], 2)

        self.assertEqual(last[2][0], -1)
        self.assertEqual(last[2][1], 3)
        self.assertEqual(last[2][3], 2)

        self.assertEqual(last[3][1], 3)
        self.assertEqual(last[3][2], 1)
        self.assertEqual(last[3][0], -1)

    def test_floyd_warshall_5(self):
        """Test the Floyd-Warshall algorithm on the graph from Figure 7-13."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 5.0)
        g.insert_edge(0, 3, 3.0)
        g.insert_edge(1, 0, -1.0)
        g.insert_edge(1, 2, 10.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 1, 2.0)
        g.insert_edge(3, 4, 3.0)
        g.insert_edge(4, 1, 1.0)
        g.insert_edge(4, 2, 4.0)

        last = FloydWarshall(g)
        self.assertEqual(len(last), 5)
        for i in range(5):
            self.assertEqual(len(last[i]), 5)

        self.assertEqual(last[0][0], -1)
        self.assertEqual(last[0][1], 0)
        self.assertEqual(last[0][2], 4)
        self.assertEqual(last[0][3], 0)
        self.assertEqual(last[0][4], 3)

        self.assertEqual(last[1][0], 1)
        self.assertEqual(last[1][1], -1)
        self.assertEqual(last[1][2], 4)
        self.assertEqual(last[1][3], 1)
        self.assertEqual(last[1][4], 3)

        self.assertEqual(last[2][0], 1)
        self.assertEqual(last[2][1], 2)
        self.assertEqual(last[2][2], -1)
        self.assertEqual(last[2][3], 1)
        self.assertEqual(last[2][4], 3)

        self.assertEqual(last[3][0], 1)
        self.assertEqual(last[3][1], 4)
        self.assertEqual(last[3][2], 4)
        self.assertEqual(last[3][3], -1)
        self.assertEqual(last[3][4], 3)

        self.assertEqual(last[4][0], 1)
        self.assertEqual(last[4][1], 4)
        self.assertEqual(last[4][2], 4)
        self.assertEqual(last[4][3], 1)
        self.assertEqual(last[4][4], -1)

    def test_floyd_warshall_5b(self):
        """Test the Floyd-Warshall algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 0.5)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 3, 2.1)
        g.insert_edge(2, 3, 5.0)
        g.insert_edge(3, 2, 5.0)
        g.insert_edge(2, 4, 0.7)
        g.insert_edge(3, 4, 2.5)
        g.insert_edge(4, 0, 2.5)

        last = FloydWarshall(g)
        self.assertEqual(len(last), 5)
        for i in range(5):
            self.assertEqual(len(last[i]), 5)

        self.assertEqual(last[0][0], -1)
        self.assertEqual(last[0][1], 0)
        self.assertEqual(last[0][2], 0)
        self.assertEqual(last[0][3], 1)
        self.assertEqual(last[0][4], 2)

        self.assertEqual(last[1][0], 4)
        self.assertEqual(last[1][1], -1)
        self.assertEqual(last[1][2], 3)
        self.assertEqual(last[1][3], 1)
        self.assertEqual(last[1][4], 3)

        self.assertEqual(last[2][0], 4)
        self.assertEqual(last[2][1], 0)
        self.assertEqual(last[2][2], -1)
        self.assertEqual(last[2][3], 2)
        self.assertEqual(last[2][4], 2)

        self.assertEqual(last[3][0], 4)
        self.assertEqual(last[3][1], 0)
        self.assertEqual(last[3][2], 3)
        self.assertEqual(last[3][3], -1)
        self.assertEqual(last[3][4], 3)

        self.assertEqual(last[4][0], 4)
        self.assertEqual(last[4][1], 0)
        self.assertEqual(last[4][2], 0)
        self.assertEqual(last[4][3], 1)
        self.assertEqual(last[4][4], -1)

    def test_floyd_warshall_5c(self):
        """Test the Floyd-Warshall algorithm on a sample graph."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 3.5)
        g.insert_edge(0, 2, 0.5)
        g.insert_edge(0, 3, 2.0)
        g.insert_edge(1, 0, 2.5)
        g.insert_edge(1, 4, 0.5)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        g.insert_edge(3, 4, 3.0)
        g.insert_edge(4, 1, 1.0)

        last = FloydWarshall(g)

        self.assertEqual(last[0][0], -1)
        self.assertEqual(last[0][1], 3)
        self.assertEqual(last[0][2], 0)
        self.assertEqual(last[0][3], 2)
        self.assertEqual(last[0][4], 1)

        self.assertEqual(last[1][0], 1)
        self.assertEqual(last[1][1], -1)
        self.assertEqual(last[1][2], 0)
        self.assertEqual(last[1][3], 2)
        self.assertEqual(last[1][4], 1)

        self.assertEqual(last[2][0], 1)
        self.assertEqual(last[2][1], 3)
        self.assertEqual(last[2][2], -1)
        self.assertEqual(last[2][3], 2)
        self.assertEqual(last[2][4], 1)

        self.assertEqual(last[3][0], 1)
        self.assertEqual(last[3][1], 3)
        self.assertEqual(last[3][2], 0)
        self.assertEqual(last[3][3], -1)
        self.assertEqual(last[3][4], 1)

        self.assertEqual(last[4][0], 1)
        self.assertEqual(last[4][1], 4)
        self.assertEqual(last[4][2], 0)
        self.assertEqual(last[4][3], 2)
        self.assertEqual(last[4][4], -1)

    def test_floyd_warshall_9(self):
        """Test the Floyd-Warshall algorithm on a sample graph."""
        g = Graph(9, undirected=False)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(0, 1, 1.0)
        g.insert_edge(1, 0, 0.5)
        g.insert_edge(1, 2, 1.5)
        g.insert_edge(1, 2, 2.0)
        g.insert_edge(2, 0, 6.0)
        g.insert_edge(2, 1, 3.0)
        g.insert_edge(2, 5, 5.0)
        g.insert_edge(3, 6, 2.0)
        g.insert_edge(3, 0, 1.5)
        g.insert_edge(4, 1, 3.0)
        g.insert_edge(4, 2, 5.0)
        g.insert_edge(4, 3, -0.5)
        g.insert_edge(4, 5, 1.0)
        g.insert_edge(4, 7, 4.0)
        g.insert_edge(5, 8, 2.0)
        g.insert_edge(6, 3, 1.0)
        g.insert_edge(6, 7, 0.5)
        g.insert_edge(7, 4, 1.0)
        g.insert_edge(8, 5, -1.0)
        g.insert_edge(8, 7, 3.0)

        last_mat = FloydWarshall(g)
        for i in range(9):
            last_vec = BellmanFord(g, i)
            self.assertEqual(last_mat[i], last_vec)

        g.insert_edge(2, 8, 1.0)
        g.insert_edge(4, 8, -0.5)

        last_mat = FloydWarshall(g)
        for i in range(9):
            last_vec = BellmanFord(g, i)
            self.assertEqual(last_mat[i], last_vec)

    def test_diameter_3(self):
        """Test computing the graph's diameter."""
        g = Graph(3, undirected=False)
        g.insert_edge(0, 1, 1.0)
        self.assertGreater(GraphDiameter(g), 100000.0)

        g.insert_edge(1, 2, 1.0)
        g.insert_edge(2, 0, 3.0)
        self.assertEqual(GraphDiameter(g), 4.0)

    def test_diameter_4(self):
        """Test computing the graph's diameter."""
        g = Graph(4, undirected=False)
        g.insert_edge(0, 1, 10.0)
        g.insert_edge(0, 2, 1.0)
        g.insert_edge(1, 2, 3.0)
        g.insert_edge(2, 3, 1.0)
        g.insert_edge(3, 1, 1.0)
        self.assertGreater(GraphDiameter(g), 100000.0)

        g.insert_edge(2, 0, 5.0)
        self.assertEqual(GraphDiameter(g), 9.0)

        g.insert_edge(3, 2, 2.0)
        self.assertEqual(GraphDiameter(g), 8.0)

    def test_diameter_5(self):
        """Test computing the graph's diameter."""
        g = Graph(5, undirected=False)
        g.insert_edge(0, 1, 5.0)
        g.insert_edge(0, 3, 3.0)
        g.insert_edge(1, 0, -1.0)
        g.insert_edge(1, 2, 10.0)
        g.insert_edge(1, 3, 1.0)
        g.insert_edge(2, 1, 2.0)
        g.insert_edge(3, 4, 3.0)
        g.insert_edge(4, 1, 1.0)
        g.insert_edge(4, 2, 4.0)

        self.assertEqual(GraphDiameter(g), 10.0)


if __name__ == "__main__":
    unittest.main()
