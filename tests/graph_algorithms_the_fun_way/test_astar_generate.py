import unittest

from graph_algorithms_the_fun_way.astar_generate import astar_dynamic, World
from graph_algorithms_the_fun_way.graph import Graph


class TestAStarGenerate(unittest.TestCase):
    def test_build_graph_from_points(self):
        """Test the dynamic A* search from Figure 8-8."""
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

        g.nodes[0].label = [0, 0]
        g.nodes[1].label = [0, 2]
        g.nodes[2].label = [2, 2]
        g.nodes[3].label = [3, 0]
        g.nodes[4].label = [1, 3]
        g.nodes[5].label = [4, 1]
        g.nodes[6].label = [3, 4]

        p = World(g, 0, 6)
        last = astar_dynamic(p)

        expected = [-1, 0, 0, 0, 1, 6, 4]
        for i in range(7):
            self.assertEqual(last[i], expected[i])


if __name__ == "__main__":
    unittest.main()
