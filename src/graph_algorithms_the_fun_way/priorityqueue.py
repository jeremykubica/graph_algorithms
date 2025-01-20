"""The core data structures for the priority queue.

This module provides example code from Jeremy Kubica's book
Graph Algorithms the Fun Way (No Starch Press 2024). As noted
in the book the code is provided for illustration purposes only.
The code written to match the explanations in the text and is NOT
fully optimized and does not include all the validity checks that
I would normally recommend in production code.
"""

from typing import Union


class HeapItem:
    """An item in the priority queue.

    Attributes
    ----------
    value : any
        The information stored in the node.
    priority : float
        The numerical priority.
    """

    def __init__(self, value, priority: float):
        self.value = value
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority


class PriorityQueue:
    """A modifiable priority queue.

    Attributes
    ----------
    array_size : int
        The size of the array storing the priority queue.
    heap_array : list of HeapItem
        The list storing the priority queue (1 indexed).
    indices : dict
        A dictionary mapping the node's value to its location in the heap list.
    is_min_heap : bool
        Indicates whether the heap is a min heap (True) or a max heap (False).
    last_index : int
        The index of the last element in the priority queue. Since the
        list is 1 indexed, a value of 0 represents an empty heap.
    """

    def __init__(self, size: int = 100, min_heap: bool = False):
        self.array_size: int = size
        self.heap_array: list = [None] * size
        self.last_index: int = 0
        self.is_min_heap: bool = min_heap
        self.indices: dict = {}

    def __len__(self):
        return self.last_index

    def size(self) -> int:
        """Return the size of the priority queue."""
        return self.last_index

    def is_empty(self) -> bool:
        """Return whether the priority queue is empty."""
        return self.last_index == 0

    def in_queue(self, value) -> bool:
        """Check if a value is in the priority queue.

        Parameters
        ----------
        value : any
            The value to look up.

        Returns
        -------
        result : bool
            True if the value is in the priority queue and False otherwise.
        """
        return value in self.indices

    def get_priority(self, value) -> Union[float, None]:
        """Look up the priority of an item in the priority queue.

        Parameters
        ----------
        value : any
            The value to look up.

        Returns
        -------
        result : float or None
            If the value is in the priority queue, the function returns
            the numerical priority. Otherwise it returns None.
        """
        if not value in self.indices:
            return None
        ind: int = self.indices[value]
        return self.heap_array[ind].priority

    def is_valid(self, verbose=False):
        """A helper function to check that the priority queue is valid
        (e.g. the heap array is in the correct order).

        Parameters
        ----------
        verbose : bool
            Output verbose debugging information.

        Returns
        -------
        result : bool
            Returns True if the priority queue is value and False otherwise.
        """
        if len(self.indices) != self.last_index:
            if verbose:
                print("PriorityQueue heap size=%i, dictionary size=%i" % (self.last_index, len(self.indices)))
            return False

        # Check that the heap is in the correct order.
        for x in range(2, self.last_index + 1):
            parent = int(x / 2)

            if not self.is_min_heap and self.heap_array[parent] < self.heap_array[x]:
                if verbose:
                    print(
                        "Error found value greater than parent %f vs %f"
                        % (self.heap_array[x].priority, self.heap_array[parent].priority)
                    )
                return False
            if self.is_min_heap and self.heap_array[parent] > self.heap_array[x]:
                if verbose:
                    print(
                        "Error found value less than parent %f vs %f"
                        % (self.heap_array[x].priority, self.heap_array[parent].priority)
                    )
                return False

        # Check that all the dictionary entries map to value heap entries.
        for value, index in self.indices.items():
            if index < 1 or index > self.last_index:
                if verbose:
                    print("Invalid PQ dictionary index: %i" % index)
                    return False
                item = self.heap_array[index]
                if item is None:
                    if verbose:
                        print("Found no item for value = ", value)
                    return False
                if item.value != value:
                    if verbose:
                        print("Value mismatch for item ", ind, ": [", item.value, "] vs [", value, "]")
                    return False

        return True

    def _swap_elements(self, index1: int, index2: int):
        """Swap two elements in the heap array.

        Parameters
        ----------
        index1 : int
            The index of the first element to swap.
        index2 : int
            The index of the second element to swap.
        """
        if index1 < 1 or index1 > self.last_index:
            return
        if index2 < 1 or index2 > self.last_index:
            return

        item1: HeapItem = self.heap_array[index1]
        item2: HeapItem = self.heap_array[index2]
        self.heap_array[index1] = item2
        self.heap_array[index2] = item1

        self.indices[item1.value] = index2
        self.indices[item2.value] = index1

    def _elements_inverted(self, parent: int, child: int) -> bool:
        """Check if two elements in the priority queue are in the wrong order.

        Parameters
        ----------
        parent : int
            The index of the parent element.
        child : int
            The index of the child element.

        Returns
        -------
        True if the objects are out of order and False otherwise.
        """
        if parent < 1 or parent > self.last_index:
            return False
        if child < 1 or child > self.last_index:
            return False

        if self.is_min_heap:
            return self.heap_array[parent] > self.heap_array[child]
        else:
            return self.heap_array[parent] < self.heap_array[child]

    def _propagate_up(self, index: int):
        """Swap the element at a given index up in the heap until it is in the
        correct location.

        Parameters
        ----------
        index : int
            The index of the element to swap up.
        """
        parent: int = int(index / 2)
        while self._elements_inverted(parent, index):
            self._swap_elements(parent, index)
            index = parent
            parent = int(index / 2)

    def _propagate_down(self, index: int):
        """Swap the element at a given index down in the heap until it is in the
        correct location.

        Parameters
        ----------
        index : int
            The index of the element to swap down.
        """
        while index <= self.last_index:
            swap: int = index
            if self._elements_inverted(swap, 2 * index):
                swap = 2 * index
            if self._elements_inverted(swap, 2 * index + 1):
                swap = 2 * index + 1

            if index != swap:
                self._swap_elements(index, swap)
                index = swap
            else:
                break

    def enqueue(self, value, priority: float):
        """Add an element to the priority queue.

        Parameters
        ----------
        value : any
            The value to insert.
        priority : float
            The value's priority.
        """
        if value in self.indices:
            self.update_priority(value, priority)
            return

        if self.last_index == self.array_size - 1:
            old_array: list = self.heap_array
            self.heap_array = [None] * self.array_size * 2
            for i in range(self.last_index + 1):
                self.heap_array[i] = old_array[i]
            self.array_size = self.array_size * 2

        self.last_index = self.last_index + 1
        self.heap_array[self.last_index] = HeapItem(value, priority)
        self.indices[value] = self.last_index
        self._propagate_up(self.last_index)

    def dequeue(self):
        """Remove and return the first element in the priority queue.

        Returns
        -------
        value : any
            The item in the priority queue.
        """
        if self.last_index == 0:
            return None

        result: HeapItem = self.heap_array[1]
        new_top: HeapItem = self.heap_array[self.last_index]
        self.heap_array[1] = new_top
        self.indices[new_top.value] = 1

        self.heap_array[self.last_index] = None
        self.indices.pop(result.value)
        self.last_index = self.last_index - 1

        self._propagate_down(1)
        return result.value

    def update_priority(self, value, priority: float):
        """Update the priority of an item in the priority queue.

        Parameters
        ----------
        value : any
            The value to update.
        priority : float
            The value's new priority.
        """
        if not value in self.indices:
            return

        index: int = self.indices[value]
        old_priority: float = self.heap_array[index].priority
        self.heap_array[index].priority = priority

        if self.is_min_heap:
            if old_priority > priority:
                self._propagate_up(index)
            else:
                self._propagate_down(index)
        else:
            if old_priority > priority:
                self._propagate_down(index)
            else:
                self._propagate_up(index)

    def peak_top(self) -> Union[HeapItem, None]:
        """Return the top HeapItem on the queue without modifying the queue.

        Returns
        -------
        top : HeapItem
            The topmost item.
        """
        if self.is_empty():
            return None
        return self.heap_array[1]

    def peek_top_priority(self) -> Union[float, None]:
        """Return the top item's priority without modifying the queue.

        Returns
        -------
        priority : float
            The priority of the topmost item.
        """
        obj: Union[HeapItem, None] = self.peak_top()
        if not obj:
            return None
        return obj.priority

    def peek_top_value(self):
        """Return the top item's value without modifying the queue.

        Returns
        -------
        value : any
            The value of the topmost item.
        """
        obj: Union[HeapItem, None] = self.peak_top()
        if not obj:
            return None
        return obj.value

    def pretty_print(self):
        """Display the priority queue in a human readable format."""
        print("PriorityQueue (MinHeap=%s) with %i items." % (str(self.is_min_heap), self.last_index))
        for i in range(1, self.last_index + 1):
            item = self.heap_array[i]
            print("%i) %s : %f" % (i, str(item.value), item.priority))


def pq_sort(arr, reverse=False):
    """Sort values using a priority queue.

    Parameters
    ----------
    arr : list
        The list of values to sort.
    reverse : bool
        If True sorts in reverse order.

    Returns
    -------
    new_array : list
        The list of values in sorted order.
    """
    n = len(arr)
    h = PriorityQueue(n, min_heap=(not reverse))
    new_array = [0] * n

    for j in range(n):
        h.enqueue(arr[j], arr[j])
    for j in range(n):
        new_array[j] = h.dequeue()

    return new_array
