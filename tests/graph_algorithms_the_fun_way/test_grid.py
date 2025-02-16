import unittest

from graph_algorithms_the_fun_way.grid import make_grid_graph, make_grid_with_obstacles
from graph_algorithms_the_fun_way.search import breadth_first_search


class TestMaze(unittest.TestCase):
    def test_make_grid(self):
        """Construct an empty 3 x 4 grid."""
        w = 3
        h = 4
        g = make_grid_graph(w, h)

        for r1 in range(h):
            for c1 in range(w):
                for r2 in range(h):
                    for c2 in range(w):
                        ind1 = r1 * w + c1
                        ind2 = r2 * w + c2

                        if abs(c1 - c2) == 1 and (r1 == r2):
                            self.assertTrue(g.is_edge(ind1, ind2))
                        elif abs(r1 - r2) == 1 and (c1 == c2):
                            self.assertTrue(g.is_edge(ind1, ind2))
                        else:
                            self.assertFalse(g.is_edge(ind1, ind2))

    def test_make_grid_large(self):
        """Construct an empty 9 x 13 grid."""
        w = 9
        h = 13

        g = make_grid_graph(w, h)
        for ind in range(w * h):
            num_edges = g.nodes[ind].num_edges()
            if ind < w:
                if ind == 0 or ind == w - 1:
                    self.assertEqual(num_edges, 2)
                else:
                    self.assertEqual(num_edges, 3)
            elif ind >= (h - 1) * w:
                if ind == (h - 1) * w or ind == h * w - 1:
                    self.assertEqual(num_edges, 2)
                else:
                    self.assertEqual(num_edges, 3)
            elif ind % w == 0:
                self.assertEqual(num_edges, 3)
            elif ind % w == w - 1:
                self.assertEqual(num_edges, 3)
            else:
                self.assertEqual(num_edges, 4)

    def test_make_grid_obstacles_small(self):
        """Construct a 3 x 4 grid with obstacles."""
        w = 4
        h = 3

        obstacles = set([(1, 2), (1, 3)])
        g = make_grid_with_obstacles(w, h, obstacles)

        self.assertEqual(g.nodes[0].num_edges(), 2)
        self.assertEqual(g.nodes[1].num_edges(), 3)
        self.assertEqual(g.nodes[2].num_edges(), 2)
        self.assertEqual(g.nodes[3].num_edges(), 1)
        self.assertEqual(g.nodes[4].num_edges(), 3)
        self.assertEqual(g.nodes[5].num_edges(), 3)
        self.assertEqual(g.nodes[6].num_edges(), 0)
        self.assertEqual(g.nodes[7].num_edges(), 0)
        self.assertEqual(g.nodes[8].num_edges(), 2)
        self.assertEqual(g.nodes[9].num_edges(), 3)
        self.assertEqual(g.nodes[10].num_edges(), 2)
        self.assertEqual(g.nodes[11].num_edges(), 1)

        self.assertEqual(g.nodes[0].label, "000_000")
        self.assertEqual(g.nodes[1].label, "000_001")
        self.assertEqual(g.nodes[2].label, "000_002")
        self.assertEqual(g.nodes[3].label, "000_003")
        self.assertEqual(g.nodes[4].label, "001_000")
        self.assertEqual(g.nodes[5].label, "001_001")
        self.assertEqual(g.nodes[6].label, "Blocked")
        self.assertEqual(g.nodes[7].label, "Blocked")
        self.assertEqual(g.nodes[8].label, "002_000")
        self.assertEqual(g.nodes[9].label, "002_001")
        self.assertEqual(g.nodes[10].label, "002_002")
        self.assertEqual(g.nodes[11].label, "002_003")

    def test_make_grid_obstacles(self):
        """Construct a 4 x 5 grid with obstacles."""
        w = 4
        h = 5

        obstacles = set([(1, 1), (2, 2), (4, 3), (1, 3)])
        g = make_grid_with_obstacles(w, h, obstacles)

        for r1 in range(h):
            for c1 in range(w):
                ind1 = r1 * w + c1
                valid1 = (r1, c1) not in obstacles
                if not valid1:
                    self.assertEqual(g.nodes[ind1].label, "Blocked")
                    self.assertEqual(len(g.nodes[ind1].edges), 0)
                else:
                    self.assertEqual(g.nodes[ind1].label, f"{r1:03d}_{c1:03d}")

                for r2 in range(h):
                    for c2 in range(w):
                        ind2 = r2 * w + c2
                        valid2 = (r2, c2) not in obstacles
                        if not valid2:
                            self.assertEqual(g.nodes[ind2].label, "Blocked")
                        else:
                            self.assertEqual(g.nodes[ind2].label, f"{r2:03d}_{c2:03d}")

                        if abs(c1 - c2) == 1 and (r1 == r2) and valid1 and valid2:
                            self.assertTrue(g.is_edge(ind1, ind2))
                        elif abs(r1 - r2) == 1 and (c1 == c2) and valid1 and valid2:
                            self.assertTrue(g.is_edge(ind1, ind2))
                        else:
                            self.assertFalse(g.is_edge(ind1, ind2))


if __name__ == "__main__":
    unittest.main()
