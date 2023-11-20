from Implementations.Queue_implementations import ArrayQueue
from Implementations.Queue_implementations import LinkedListQueue
from Implementations.Queue_implementations import CircularBufferQueue
from Implementations.Stack_implementations import ArrayStack
from Implementations.Stack_implementations import LinkedListStack
from Implementations.Stack_implementations import DoubleStack

class Menu:
    def __init__(self):
        self.queues = {}
        self.stacks = {}

    def run(self):
        while True:
            print("\nMenu:")
            print("1. Create Queue")
            print("2. Create Stack")
            print("3. Perform Queue Operations")
            print("4. Perform Stack Operations")
            print("5. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                self.create_queue()
            elif choice == '2':
                self.create_stack()
            elif choice == '3':
                self.queue_operations()
            elif choice == '4':
                self.stack_operations()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_queue(self):
        print("Select type of Queue to create:")
        print("1. ArrayQueue")
        print("2. LinkedListQueue")
        print("3. CircularBufferQueue")
        choice = input("Enter choice: ")
        name = input("Enter a name for your Queue: ")
        if choice == '1':
            self.queues[name] = ArrayQueue()
        elif choice == '2':
            self.queues[name] = LinkedListQueue()
        elif choice == '3':
            self.queues[name] = CircularBufferQueue()
        else:
            print("Invalid choice.")

    def create_stack(self):
        print("Select type of Stack to create:")
        print("1. ArrayStack")
        print("2. LinkedListStack")
        print("3. DoubleStack")
        choice = input("Enter choice: ")
        name = input("Enter a name for your Stack: ")
        if choice == '1':
            self.stacks[name] = ArrayStack()
        elif choice == '2':
            self.stacks[name] = LinkedListStack()
        elif choice == '3':
            self.stacks[name] = DoubleStack()
        else:
            print("Invalid choice.")

    def queue_operations(self):
        queue_name = input("Enter the name of the queue you want to operate on: ")
        if queue_name not in self.queues:
            print("Queue not found.")
            return

        queue = self.queues[queue_name]
        while True:
            print("\nQueue Operations:")
            print("1. Enqueue")
            print("2. Dequeue")
            print("3. Peek")
            print("4. Check if Empty")
            print("5. Check if Full")
            print("6. Return to Main Menu")
            choice = input("Enter choice: ")

            if choice == '1':
                item = input("Enter the item to enqueue: ")
                try:
                    queue.enqueue(item)
                    print(f"Enqueued {item}.")
                except Exception as e:
                    print(str(e))
            elif choice == '2':
                try:
                    item = queue.dequeue()
                    print(f"Dequeued: {item}")
                except Exception as e:
                    print(str(e))
            elif choice == '3':
                try:
                    item = queue.peek()
                    print(f"Front item: {item}")
                except Exception as e:
                    print(str(e))
            elif choice == '4':
                print("Queue is empty." if queue.is_empty() else "Queue is not empty.")
            elif choice == '5':
                print("Queue is full." if queue.is_full() else "Queue is not full.")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def stack_operations(self):
        stack_name = input("Enter the name of the stack you want to operate on: ")
        if stack_name not in self.stacks:
            print("Stack not found.")
            return

        stack = self.stacks[stack_name]
        while True:
            print("\nStack Operations:")
            print("1. Push")
            print("2. Pop")
            print("3. Peek")
            print("4. Check if Empty")
            print("5. Check if Full")
            print("6. Return to Main Menu")
            choice = input("Enter choice: ")

            if choice == '1':
                item = input("Enter the item to push: ")
                try:
                    stack.push(item)
                    print(f"Pushed {item}.")
                except Exception as e:
                    print(str(e))
            elif choice == '2':
                try:
                    item = stack.pop()
                    print(f"Popped: {item}")
                except Exception as e:
                    print(str(e))
            elif choice == '3':
                try:
                    item = stack.peek()
                    print(f"Top item: {item}")
                except Exception as e:
                    print(str(e))
            elif choice == '4':
                print("Stack is empty." if stack.is_empty() else "Stack is not empty.")
            elif choice == '5':
                print("Stack is full." if stack.is_full() else "Stack is not full.")
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")