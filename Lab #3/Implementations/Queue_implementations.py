from Classes.Queue import AbstractQueue
from Classes.Node import Node

# ======================
# Array implementation
# ======================

class ArrayQueue(AbstractQueue):
    def __init__(self):
        self.items = []
        self.capacity = 5

    def enqueue(self,item):
        if self.is_full():
            raise IndexError("Queue is full. Cannot enqueue")
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeu from empty queue")
        self.items.pop(0)
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0
    
    def is_full(self):
        return len(self.items) == capacity

# =========================================================
# Linked list implementation (we use additional Node class)
# =========================================================

class LinkedListQueue(AbstractQueue):
    def __init__(self):
        self.head = head
        self.tail = tail

    def enqueue(self,item):
        new_node = Node(item)
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node 

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeu from an empty queue")
        ret_val = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return ret_val
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.data

    def is_empty(self):
        return self.head == None

# ==========================
# Circular Buffer implementation
# ==========================

class CircularBufferQueue(AbstractQueue):
    def __init__(self, capacity = 5):
        self.items = [None] * capacity
        self.size = 0
        self.front = 0
        self.rear = 0
     
    def enqueue(self,item):
        if self.is_full():
            raise IndexError("Queue is full. Cannot enqueue")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % len(self._items)
        self._size += 1

    def dequeue(self):
        pass

    def peek(self):
        pass

    def is_empty(self):
        pass

    def is_full(self):
        return self._size == len(self._items)



# ========================================================================

# Implementation of Queue using a Python list (ArrayQueue)
class ArrayQueue(AbstractQueue):
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        if not self.is_full():
            raise IndexError("")
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def is_full(self):
        return 


# Implementation of Queue using a linked list (LinkedListQueue)
class LinkedListQueue(AbstractQueue):
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        ret_value = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return ret_value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self.head.data

    def is_empty(self):
        return self.head is None


# Implementation of Queue using a circular buffer (CircularBufferQueue)
class CircularBufferQueue(AbstractQueue):
    def __init__(self, capacity=5):
        self._items = [None] * capacity
        self._size = 0
        self._front = 0
        self._rear = 0

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("enqueue in a full queue")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % len(self._items)
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        ret_value = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % len(self._items)
        self._size -= 1
        return ret_value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[self._front]

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == len(self._items)
