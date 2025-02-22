from graph_algorithms_the_fun_way.priorityqueue import PriorityQueue, pq_sort

import unittest


def is_sorted(arr) -> bool:
    """A helper function that checks if a list of values is sorted.

    Parameters
    ----------
    arr : list
        The list of values.

    Returns
    -------
    result : bool
        True if the list is sorted and False otherwise.
    """
    n: int = len(arr)
    for i in range(n - 1):
        if arr[i] < arr[i + 1]:
            return False
    return True


class TestPriorityQueue(unittest.TestCase):
    def test_is_empty(self):
        """Test the is_empty function."""
        pq = PriorityQueue(10)
        self.assertTrue(pq.is_empty())

        pq.enqueue(10.0, 100.0)
        self.assertFalse(pq.is_empty())

        pq.enqueue(11.0, 99.0)
        self.assertFalse(pq.is_empty())

    def test_enqueue_1(self):
        """First test case for inserting values into a max heap."""
        pq = PriorityQueue(10)
        self.assertEqual(pq.size(), 0)

        arr = [46, 35, 9, 28, 61, 8, 38, 40]
        for i in range(len(arr)):
            self.assertFalse(pq.in_queue(i))

        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))
            self.assertTrue(pq.in_queue(i))
            self.assertEqual(pq.get_priority(i), arr[i])
            self.assertFalse(pq.in_queue(i + 1))

            p1 = pq.peek_top_priority()
            p2 = max(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)

        self.assertEqual(pq.peek_top_value(), 4)

    def test_enqueue_min_1(self):
        """First test case for inserting values into a min heap."""
        pq = PriorityQueue(10, min_heap=True)
        self.assertEqual(pq.size(), 0)

        arr = [46, 35, 9, 28, 61, 8, 38, 40]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))

            p1 = pq.peek_top_priority()
            p2 = min(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)
        self.assertEqual(pq.peek_top_value(), 5)

    def test_enqueue_2(self):
        """Second test case for inserting values into a max heap.
        Inserts values in increasing order.
        """
        pq = PriorityQueue(10)
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))

            p1 = pq.peek_top_priority()
            p2 = max(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)

    def test_enqueue_min_2(self):
        """Second test case for inserting values into a min heap.
        Inserts values in increasing order.
        """
        pq = PriorityQueue(10, min_heap=True)
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))

            p1 = pq.peek_top_priority()
            p2 = min(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)

    def test_enqueue_3(self):
        """Third test case for inserting values into a max heap.
        Inserts value in decreasing order."""
        pq = PriorityQueue(10)
        arr = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))

            p1 = pq.peek_top_priority()
            p2 = max(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)

    def test_enqueue_min_3(self):
        """Third test case for inserting values into a min heap.
        Inserts value in decreasing order."""
        pq = PriorityQueue(10, min_heap=True)
        arr = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])
            self.assertEqual(pq.size(), i + 1)
            self.assertTrue(pq.is_valid(True))

            p1 = pq.peek_top_priority()
            p2 = min(arr[0 : (i + 1)])
            self.assertEqual(p1, p2)

    def test_update_priority(self):
        """Test that we can update priorities."""
        pq = PriorityQueue(10)
        arr = [46, 35, 9, 28, 61, 8, 38, 40]
        for i in range(len(arr)):
            pq.enqueue(i, arr[i])

        pq.update_priority(5, 39)
        self.assertTrue(pq.is_valid(True))
        self.assertTrue(pq.in_queue(5))
        self.assertEqual(pq.get_priority(5), 39)

        pq.update_priority(0, 29)
        self.assertTrue(pq.is_valid(True))
        self.assertTrue(pq.in_queue(0))
        self.assertEqual(pq.get_priority(0), 29)

    def test_remove_max(self):
        """Test that we can dequeue elements in a max heap."""
        pq = PriorityQueue(20)
        arr = [46, 35, 9, 28, 61, 8, 38, 40, 100, 5, 4, 3, 50, 51]
        for i in range(len(arr)):
            pq.enqueue(arr[i], arr[i])

        s_arr = sorted(arr, reverse=True)
        for i in range(len(arr)):
            key = pq.dequeue()
            self.assertEqual(key, s_arr[i])
            self.assertTrue(pq.is_valid(True))
            self.assertFalse(pq.in_queue(key))

    def test_remove_min(self):
        """Test that we can dequeue elements in a min heap."""
        pq = PriorityQueue(20, min_heap=True)
        arr = [46, 35, 9, 28, 61, 8, 38, 40, 100, 5, 4, 3, 50, 51]
        for i in range(len(arr)):
            pq.enqueue(arr[i], arr[i])

        s_arr = sorted(arr, reverse=False)
        for i in range(len(arr)):
            key = pq.dequeue()
            self.assertEqual(key, s_arr[i])
            self.assertTrue(pq.is_valid(True))
            self.assertFalse(pq.in_queue(key))

    def test_pq_sort_descending(self):
        """Test that we can use the PriorityQueue to sort elements."""
        s = pq_sort([10, -1, 0, 5, 3, 4, -5, 20], reverse=True)
        self.assertEqual(s, [20, 10, 5, 4, 3, 0, -1, -5])

        s = pq_sort([1, 2, 3, 4, 5], reverse=True)
        self.assertEqual(s, [5, 4, 3, 2, 1])

        s = pq_sort([0, 1, -1, 2, -2, -3, 3, 4, -4, -5, 5], reverse=True)
        self.assertEqual(s, [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5])

    def test_pq_sort_ascending(self):
        """Test that we can use the PriorityQueue to sort elements."""
        s = pq_sort([10, -1, 0, 5, 3, 4, -5, 20])
        self.assertEqual(s, [-5, -1, 0, 3, 4, 5, 10, 20])

        s = pq_sort([1, 2, 3, 4, 5])
        self.assertEqual(s, [1, 2, 3, 4, 5])

        s = pq_sort([0, 1, -1, 2, -2, -3, 3, 4, -4, -5, 5])
        self.assertEqual(s, [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

    def test_dynamic(self):
        """Test that we can insert, modify, and remove elements using a max heap."""
        pq = PriorityQueue()

        pq.enqueue("A", 100.0)
        pq.enqueue("B", 0.0)
        pq.enqueue("C", 50.0)
        pq.enqueue("D", 25.0)
        pq.enqueue("E", 10.0)
        pq.enqueue("F", 75.0)
        pq.enqueue("G", 55.0)
        pq.enqueue("H", 20.0)
        pq.enqueue("I", 15.0)
        pq.enqueue("J", 30.0)
        pq.enqueue("K", 40.0)
        pq.enqueue("L", 45.0)
        pq.enqueue("M", 85.0)
        self.assertTrue(pq.is_valid(True))

        # Update some priorities
        pq.enqueue("A", 70.0)
        pq.update_priority("I", 60.0)
        pq.update_priority("L", 35.0)
        self.assertTrue(pq.is_valid(True))

        # Check we get things in the correct order.
        self.assertEqual(pq.dequeue(), "M")
        self.assertEqual(pq.dequeue(), "F")
        self.assertEqual(pq.dequeue(), "A")
        self.assertEqual(pq.dequeue(), "I")
        self.assertEqual(pq.dequeue(), "G")
        self.assertEqual(pq.dequeue(), "C")
        self.assertEqual(pq.dequeue(), "K")
        self.assertEqual(pq.dequeue(), "L")
        self.assertEqual(pq.dequeue(), "J")
        self.assertEqual(pq.dequeue(), "D")
        self.assertEqual(pq.dequeue(), "H")
        self.assertEqual(pq.dequeue(), "E")
        self.assertEqual(pq.dequeue(), "B")

    def test_dynamic_reversed(self):
        """Test that we can insert, modify, and remove elements using a min heap."""
        pq = PriorityQueue(min_heap=True)

        pq.enqueue("A", 100.0)
        pq.enqueue("B", 0.0)
        pq.enqueue("C", 50.0)
        pq.enqueue("D", 25.0)
        pq.enqueue("E", 10.0)
        pq.enqueue("F", 75.0)
        pq.enqueue("G", 55.0)
        pq.enqueue("H", 20.0)
        pq.enqueue("I", 15.0)
        pq.enqueue("J", 30.0)
        pq.enqueue("K", 40.0)
        pq.enqueue("L", 45.0)
        pq.enqueue("M", 85.0)
        self.assertTrue(pq.is_valid(True))

        # Update some priorities
        pq.enqueue("A", 70.0)
        pq.update_priority("I", 60.0)
        pq.update_priority("L", 35.0)
        self.assertTrue(pq.is_valid(True))

        # Check we get things in the correct order.
        self.assertEqual(pq.dequeue(), "B")
        self.assertEqual(pq.dequeue(), "E")
        self.assertEqual(pq.dequeue(), "H")
        self.assertEqual(pq.dequeue(), "D")
        self.assertEqual(pq.dequeue(), "J")
        self.assertEqual(pq.dequeue(), "L")
        self.assertEqual(pq.dequeue(), "K")
        self.assertEqual(pq.dequeue(), "C")
        self.assertEqual(pq.dequeue(), "G")
        self.assertEqual(pq.dequeue(), "I")
        self.assertEqual(pq.dequeue(), "A")
        self.assertEqual(pq.dequeue(), "F")
        self.assertEqual(pq.dequeue(), "M")


if __name__ == "__main__":
    unittest.main()
