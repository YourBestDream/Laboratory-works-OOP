from Classes.Stack import AbstractStack
from Classes.Node import Node

# ======================
# Array implementation
# ======================

class ArrayStack(AbstractStack):
    def __init__(self):
        self.items = []
        self.capacity = 5
    
    def push(self,item):
        if self.is_full():
            raise IndexError("The stack is full. Cannot push")
        self.items.append(item)

    def pop(self):
        if self.is_empty:
            raise IndexError("Nothing to pop")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty:
            raise IndexError("Empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0
    
    def is_full(self):
        return len(self.items) == capacity

# ==========================
# Linked list implementation
# ==========================

class LinkedListStack(AbstractStack):
    def __init__(self):
        self.head = None
        self.capacity = 5
    
    def push(self,item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack")
        ret_data = self.head.data
        self.head = self.head.next
        return ret_data

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack")
        return self.head.data

    def is_empty(self):
        return self.head is None

    def is_full(self):
        pass

# ===========================
# Double Stack implementation
# ===========================

class DoubleStack(AbstractStack):
    def __init__(self):
        self.stack_in = ArrayStack()
        self.stack_out = ArrayStack()
        self.capacity = 5

    def push(self,item):
        self.stack_in.append(item)
    
    def pop(self):
        if self.is_empty(self.stack_in):
            raise IndexError("Cannot pop from empty stack")
        if self.is_empty(self.stack_out):
            while not self.is_empty(self.stack_in):
                self.stack_out.push(self.stack_in.pop())
        return self.stack_out.pop()
        

    def peek(self):
        if self.is_empty(self.stack_in):
            raise IndexError("Cannot pop from empty stack")
        if self.is_empty(self.stack_out):
            while not self.is_empty(self.stack_in):
                self.stack_out.push(self.stack_in.pop())
        return self.stack_out.peek()

    def is_empty(self, array):
        self.array = array
        return len(self.array) == 0
    
    def is_full(self):
        pass