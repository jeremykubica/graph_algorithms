import math
import unittest

from graph_algorithms_the_fun_way.spatial_graphs import (
    build_graph_from_points,
    single_linkage_clustering,
    Point,
)


class TestGraphSpatial(unittest.TestCase):
    def setUp(self):
        self.p3 = [Point(0, 0), Point(2, 0), Point(0, 1)]

        self.p5 = [Point(0, 0), Point(1, 0), Point(1.2, 1), Point(1.8, 1), Point(0.5, 1.5)]

    def test_build_graph_from_points(self):
        """Build a graph from a list of spatial points."""
        g3 = build_graph_from_points(self.p3)
        self.assertAlmostEqual(g3.get_edge(0, 1).weight, 2.0)
        self.assertAlmostEqual(g3.get_edge(1, 0).weight, 2.0)
        self.assertAlmostEqual(g3.get_edge(0, 2).weight, 1.0)
        self.assertAlmostEqual(g3.get_edge(2, 0).weight, 1.0)
        self.assertAlmostEqual(g3.get_edge(1, 2).weight, math.sqrt(5.0))
        self.assertAlmostEqual(g3.get_edge(2, 1).weight, math.sqrt(5.0))

        g5 = build_graph_from_points(self.p5)
        for i in range(5):
            for j in range(i + 1, 5):
                dist = self.p5[i].distance(self.p5[j])
                self.assertAlmostEqual(g5.get_edge(i, j).weight, dist)
                self.assertAlmostEqual(g5.get_edge(j, i).weight, dist)

        # Test numbers in Figure A-4
        self.assertAlmostEqual(g5.get_edge(0, 1).weight, 1.00, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(0, 2).weight, 1.56, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(0, 3).weight, 2.06, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(0, 4).weight, 1.58, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(1, 0).weight, 1.00, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(1, 2).weight, 1.02, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(1, 3).weight, 1.28, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(1, 4).weight, 1.58, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(2, 0).weight, 1.56, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(2, 1).weight, 1.02, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(2, 3).weight, 0.60, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(2, 4).weight, 0.86, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(3, 0).weight, 2.06, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(3, 1).weight, 1.28, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(3, 2).weight, 0.60, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(3, 4).weight, 1.39, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(4, 0).weight, 1.58, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(4, 1).weight, 1.58, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(4, 2).weight, 0.86, delta=0.02)
        self.assertAlmostEqual(g5.get_edge(4, 3).weight, 1.39, delta=0.02)

    def test_single_linkage_clustering(self):
        """Test single-linkage clustering."""
        links3 = single_linkage_clustering(self.p3)
        self.assertEqual(len(links3), 2)
        self.assertEqual(links3[0].id1, 0)
        self.assertEqual(links3[0].id2, 2)
        self.assertAlmostEqual(links3[0].dist, 1.0)
        self.assertEqual(links3[1].id1, 0)
        self.assertEqual(links3[1].id2, 1)
        self.assertAlmostEqual(links3[1].dist, 2.0)

        for i in range(1, len(links3)):
            self.assertGreater(links3[i].dist, links3[i - 1].dist)

        links5 = single_linkage_clustering(self.p5)
        self.assertEqual(len(links5), 4)
        self.assertEqual(links5[0].id1, 2)
        self.assertEqual(links5[0].id2, 3)
        self.assertAlmostEqual(links5[0].dist, 0.6, delta=0.001)
        self.assertEqual(links5[1].id1, 2)
        self.assertEqual(links5[1].id2, 4)
        self.assertAlmostEqual(links5[1].dist, 0.860233, delta=0.001)
        self.assertEqual(links5[2].id1, 0)
        self.assertEqual(links5[2].id2, 1)
        self.assertAlmostEqual(links5[2].dist, 1.0, delta=0.001)
        self.assertEqual(links5[3].id1, 1)
        self.assertEqual(links5[3].id2, 2)
        self.assertAlmostEqual(links5[3].dist, 1.019804, delta=0.001)

        for i in range(1, len(links5)):
            self.assertGreater(links5[i].dist, links5[i - 1].dist)


if __name__ == "__main__":
    unittest.main()
