from graph_algorithms_the_fun_way.union_find import UnionFind

import unittest


class TestUnionFind(unittest.TestCase):

    def test_basic(self):
        """Test basic operations of a UnionFind data structure."""
        djs = UnionFind(3)
        self.assertEqual(djs.num_disjoint_sets, 3)
        self.assertTrue(djs.are_disjoint(0, 1))
        self.assertTrue(djs.are_disjoint(1, 2))
        self.assertTrue(djs.are_disjoint(0, 2))

        djs.union_sets(0, 1)
        self.assertEqual(djs.num_disjoint_sets, 2)
        self.assertFalse(djs.are_disjoint(0, 1))
        self.assertFalse(djs.are_disjoint(1, 0))
        self.assertTrue(djs.are_disjoint(1, 2))
        self.assertTrue(djs.are_disjoint(0, 2))

        with self.assertRaises(IndexError):
            djs.find_set(-1)
        with self.assertRaises(IndexError):
            djs.find_set(4)
        with self.assertRaises(IndexError):
            djs.are_disjoint(0, -1)
        with self.assertRaises(IndexError):
            djs.are_disjoint(4, 0)

    def test_large(self):
        """Test basic operations on a larger set of elements."""
        djs = UnionFind(20)
        self.assertEqual(djs.num_disjoint_sets, 20)

        for i in range(20):
            for j in range(20):
                if i != j:
                    self.assertTrue(djs.are_disjoint(i, j))

        # Merge half the sets
        for i in range(10):
            djs.union_sets(i, 10 + i)
        self.assertEqual(djs.num_disjoint_sets, 10)

        # Merge half the sets again
        for i in range(5):
            djs.union_sets(i, 5 + i)
        self.assertEqual(djs.num_disjoint_sets, 5)

        for i in range(5):
            self.assertFalse(djs.are_disjoint(i, i + 5))
            self.assertFalse(djs.are_disjoint(i, i + 10))
            self.assertFalse(djs.are_disjoint(i, i + 15))
            self.assertFalse(djs.are_disjoint(i + 5, i + 10))
            self.assertFalse(djs.are_disjoint(i + 10, i + 15))

            self.assertTrue(djs.are_disjoint(i, i + 1))
            self.assertTrue(djs.are_disjoint(i, i + 2))
            self.assertTrue(djs.are_disjoint(i, i + 3))
            self.assertTrue(djs.are_disjoint(i, i + 4))

    def test_merge_into_one(self):
        """Test that we can merge down into a single set."""
        djs = UnionFind(15)
        self.assertEqual(djs.num_disjoint_sets, 15)

        for i in range(15):
            for j in range(15):
                if djs.are_disjoint(i, j):
                    djs.union_sets(i, j)
        self.assertEqual(djs.num_disjoint_sets, 1)

        for i in range(15):
            for j in range(15):
                self.assertFalse(djs.are_disjoint(i, j))


if __name__ == "__main__":
    unittest.main()
