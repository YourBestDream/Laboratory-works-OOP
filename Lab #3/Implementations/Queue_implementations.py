from Classes.Queue import AbstractQueue
from Classes.Node import Node

# ======================
# Array implementation
# ======================

class ArrayQueue(AbstractQueue):
    def __init__(self):
        self.items = []

    def enqueue(self,item):
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
        pass

    def dequeue(self):
        pass

    def peek(self):
        pass

    def is_empty(self):
        pass