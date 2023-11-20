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
        return len(self.items) == self.capacity


# =========================================================
# Linked list implementation (we use additional Node class)
# =========================================================

class LinkedListQueue(AbstractQueue):
    def __init__(self, capacity=5):
        self.head = None
        self.tail = None
        self.size = 0
        self.capacity = capacity

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("Queue is full. Cannot enqueue")
        new_node = Node(item)
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node
        self.size += 1

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

    def is_full(self):
        return self.size == self.capacity

# ==========================
# Circular Buffer implementation
# ==========================

class CircularBufferQueue(AbstractQueue):
    def __init__(self, capacity=5):
        self.items = [None] * capacity
        self.size = 0
        self.front = 0
        self.rear = 0

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("Queue is full. Cannot enqueue")
        self.items[self.rear] = item
        self.rear = (self.rear + 1) % len(self.items)
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty. Cannot dequeue")
        item = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % len(self.items)
        self.size -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[self.front]

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == len(self.items)
