from abc import ABC, abstractmethod

class AbstractQueue(ABC):
    @abstractmethod
    def enqueue(self, value):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def peek(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass