class Menu:
    def __init__(self):
        # Initialize stacks and queues with different implementations
        self.stacks = {
            'ArrayStack': ArrayStack(),
            'LinkedListStack': LinkedListStack(),
            'DoubleStack': DoubleStack()
        }
        self.queues = {
            'ArrayQueue': ArrayQueue(),
            'LinkedListQueue': LinkedListQueue(),
            'CircularBufferQueue': CircularBufferQueue()
        }
        self.current_structure = None

    def main(self):
        while True:
            self.print_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.select_structure()
            elif choice == '2':
                self.perform_push()
            elif choice == '3':
                self.perform_pop()
            elif choice == '4':
                self.perform_peek()
            elif choice == '5':
                self.check_is_empty()
            elif choice == '6':
                self.exit_menu()
            else:
                print("Invalid choice, please try again.")

    def print_menu(self):
        print("""
        1. Select Data Structure
        2. Push/Enqueue
        3. Pop/Dequeue
        4. Peek
        5. Is Empty
        6. Exit
        """)

    def select_structure(self):
        choice = input("Choose a structure (Stack/Queue): ").lower()
        if choice == 'stack':
            self.current_structure = self.stacks[input("Select implementation (ArrayStack/LinkedListStack/DoubleStack): ")]
        elif choice == 'queue':
            self.current_structure = self.queues[input("Select implementation (ArrayQueue/LinkedListQueue/CircularBufferQueue): ")]
        else:
            print("Invalid choice.")

    def perform_push(self):
        if isinstance(self.current_structure, AbstractStack) or isinstance(self.current_structure, AbstractQueue):
            item = input("Enter item to push/enqueue: ")
            if isinstance(self.current_structure, AbstractStack):
                self.current_structure.push(item)
            else:
                self.current_structure.enqueue(item)
        else:
            print("No data structure selected or the selected structure does not support push/enqueue.")

    def perform_pop(self):
        if isinstance(self.current_structure, AbstractStack) or isinstance(self.current_structure, AbstractQueue):
            try:
                item = self.current_structure.pop() if isinstance(self.current_structure, AbstractStack) else self.current_structure.dequeue()
                print(f"Item {item} has been removed.")
            except IndexError as e:
                print(e)
        else:
            print("No data structure selected or the selected structure does not support pop/dequeue.")

    def perform_peek(self):
        if isinstance(self.current_structure, AbstractStack) or isinstance(self.current_structure, AbstractQueue):
            try:
                item = self.current_structure.peek()
                print(f"Item at the top/front: {item}")
            except IndexError as e:
                print(e)
        else:
            print("No data structure selected or the selected structure does not support peek.")

    def check_is_empty(self):
        if self.current_structure:
            print("The structure is empty." if self.current_structure.is_empty() else "The structure is not empty.")
        else:
            print("No data structure selected.")

    def exit_menu(self):
        print("Exiting the menu.")
        exit()
