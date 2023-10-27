# Import the os and time modules
import os
import time

# Define a class for files
class File:
    # Initialize the file attributes
    def __init__(self, name, path):
        self.name = name # The file name
        self.path = path # The file path
        self.ext = os.path.splitext(name)[1] # The file extension
        self.created = os.path.getctime(path) # The file creation time
        self.updated = os.path.getmtime(path) # The file modification time
        self.changed = False # The file change status

    # Define a method to check if the file has changed since the last snapshot
    def check_change(self, snapshot):
        # Update the modification time
        self.updated = os.path.getmtime(self.path)
        # Compare it with the snapshot time
        if self.updated > snapshot:
            # If it is greater, the file has changed
            self.changed = True
        else:
            # If it is equal or smaller, the file has not changed
            self.changed = False

    # Define a method to print general information about the file
    def info(self):
        # Print the file name and extension
        print(f"File name: {self.name}")
        print(f"File extension: {self.ext}")
        # Print the creation and modification time in a readable format
        print(f"Created at: {time.ctime(self.created)}")
        print(f"Updated at: {time.ctime(self.updated)}")

    # Define a method to count the lines in the file
    def count_lines(self):
        # Open the file in read mode
        with open(self.path, "r") as f:
            # Read all the lines and return their number
            lines = f.readlines()
            return len(lines)

# Define a subclass for image files
class ImageFile(File):
    # Import the PIL module for image processing
    from PIL import Image

    # Initialize the image file attributes by inheriting from the parent class
    def __init__(self, name, path):
        super().__init__(name, path)
        # Open the image and get its size
        self.image = Image.open(path)
        self.size = self.image.size

    # Override the info method to include the image size
    def info(self):
        # Call the parent method first
        super().info()
        # Print the image size in pixels
        print(f"Image size: {self.size[0]}x{self.size[1]}")

# Define a subclass for text files
class TextFile(File):
    # Initialize the text file attributes by inheriting from the parent class
    def __init__(self, name, path):
        super().__init__(name, path)

    # Override the info method to include the word and character count
    def info(self):
        # Call the parent method first
        super().info()
        # Open the file in read mode
        with open(self.path, "r") as f:
            # Read all the text and split it into words
            text = f.read()
            words = text.split()
            # Count the number of words and characters
            word_count = len(words)
            char_count = len(text)
            # Print the word and character count
            print(f"Word count: {word_count}")
            print(f"Character count: {char_count}")

# Define a subclass for program files
class ProgramFile(File):
    # Initialize the program file attributes by inheriting from the parent class
    def __init__(self, name, path):
        super().__init__(name, path)

    # Override the info method to include the class and method count
    def info(self):
        # Call the parent method first
        super().info()
        # Open the file in read mode
        with open(self.path, "r") as f:
            # Read all the lines and initialize the counters
            lines = f.readlines()
            class_count = 0
            method_count = 0
            # Loop through each line and check for keywords
            for line in lines:
                line = line.strip() # Remove leading and trailing spaces
                if line.startswith("class"): # If it starts with class, increment class count
                    class_count += 1 
                elif line.startswith("def"): # If it starts with def, increment method count 
                    method_count += 1 
            # Print the class and method count 
            print(f"Class count: {class_count}")
            print(f"Method count: {method_count}")

# Define a function to create a file object based on its extension 
def create_file(name, path):
    ext = os.path.splitext(name)[1] # Get the file extension 
    if ext in [".png", ".jpg"]: # If it is an image file, create an ImageFile object
        return ImageFile(name, path)
    elif ext == ".txt": # If it is a text file, create a TextFile object
        return TextFile(name, path)
    elif ext in [".py", ".java"]: # If it is a program file, create a ProgramFile object
        return ProgramFile(name, path)
    else: # Otherwise, create a generic File object
        return File(name, path)

# Define a function to print the status of the files 
def print_status(files, snapshot):
    # Loop through each file in the dictionary
    for name, file in files.items():
        # Check if the file has changed since the last snapshot
        file.check_change(snapshot)
        # Print the file name and change status
        if file.changed:
            print(f"{name} - Changed")
        else:
            print(f"{name} - No Change")

# Define a function to schedule the status check every 5 seconds 
def schedule_status(files, snapshot):
    # Import the threading module 
    import threading
    # Create a timer object that calls the print_status function after 5 seconds 
    timer = threading.Timer(5.0, print_status, args=[files, snapshot])
    # Start the timer 
    timer.start()
    # Return the timer object 
    return timer

# Define the folder path (hardcoded)
folder = "E:\programs\OOP Labs\Laboratory-works-OOP\control"

# Get the list of files in the folder 
files = os.listdir(folder)

# Create a dictionary to store the file objects 
file_dict = {}

# Loop through each file name in the list 
for file in files:
    # Get the full path of the file 
    path = os.path.join(folder, file)
    # Create a file object based on its extension and add it to the dictionary 
    file_dict[file] = create_file(file, path)

# Initialize the snapshot time as the current time 
snapshot = time.time()

# Print a welcome message and instructions 
print("Welcome to the file change detection program.")
print("The folder being monitored is:", folder)
print("The available actions are:")
print("commit - Update the snapshot time to the current time.")
print("info <filename> - Print general information about the file.")
print("status - Show the change status of each file since the last snapshot.")
print("exit - Exit the program.")

# Start the scheduler for status check 
scheduler = schedule_status(file_dict, snapshot)

# Create a loop for user input 
while True:
    # Prompt the user for an action 
    action = input("Enter an action: ")
    # Split the action into words 
    words = action.split()
    # Check if the first word is a valid action 
    if words[0] == "commit":
        # Update the snapshot time to the current time 
        snapshot = time.time()
        # Print a confirmation message 
        print(f"Created Snapshot at: {time.ctime(snapshot)}")
        # Restart the scheduler with the new snapshot time 
        scheduler.cancel()
        scheduler = schedule_status(file_dict, snapshot)
    elif words[0] == "info":
        # Check if there is a second word as filename 
        if len(words) > 1:
            # Get the filename from the second word 
            filename = words[1]
            # Check if the filename is in the dictionary 
            if filename in file_dict:
                # Get the file object from the dictionary 
                file = file_dict[filename]
                # Print general information about the file 
                file.info()
            else:
                # Print an error message 
                print(f"{filename} does not exist in {folder}")
        else:
            # Print an error message 
            print("Please enter a filename after info.")
    elif words[0] == "status":
        # Print the status of each file since the last snapshot
        print_status(file_dict, snapshot)
    elif words[0] == "exit":
        # Exit the program loop and cancel the scheduler
        break
    else:
        # Print an error message
        print("Invalid action. Please try again.")

# Print a goodbye message
print("Thank you for using the program. Goodbye.")