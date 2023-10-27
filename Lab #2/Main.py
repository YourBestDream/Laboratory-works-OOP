import os
import time
import threading # Importing the threading module

# Defining a class for files
class File:
    # Initializing the file object with name, extension, created and updated time
    def __init__(self, name, extension, created, updated):
        self.name = name
        self.extension = extension
        self.created = created
        self.updated = updated

    # Defining a method to print general information about the file
    def info(self):
        print(f"File name: {self.name}")
        print(f"File extension: {self.extension}")
        print(f"Created date and time: {self.created}")
        print(f"Updated date and time: {self.updated}")

    # Defining a method to check if the file has changed since the last snapshot
    def has_changed(self, snapshot):
        return self.updated > snapshot

# Defining a subclass for image files
class ImageFile(File):
    # Initializing the image file object with name, extension, created, updated and size
    def __init__(self, name, extension, created, updated, size):
        super().__init__(name, extension, created, updated) # Calling the superclass constructor
        self.size = size

    # Overriding the info method to print the image size as well
    def info(self):
        super().info() # Calling the superclass method
        print(f"Image size: {self.size}")

# Defining a subclass for text files
class TextFile(File):
    # Initializing the text file object with name, extension, created, updated, line count, word count and character count
    def __init__(self, name, extension, created, updated, line_count, word_count, char_count):
        super().__init__(name, extension, created, updated) # Calling the superclass constructor
        self.line_count = line_count
        self.word_count = word_count
        self.char_count = char_count

    # Overriding the info method to print the text file statistics as well
    def info(self):
        super().info() # Calling the superclass method
        print(f"Line count: {self.line_count}")
        print(f"Word count: {self.word_count}")
        print(f"Character count: {self.char_count}")

# Defining a subclass for program files
class ProgramFile(File):
    # Initializing the program file object with name, extension, created, updated and class count and method count
    def __init__(self, name, extension, created, updated, class_count, method_count):
        super().__init__(name, extension, created, updated) # Calling the superclass constructor
        self.class_count = class_count
        self.method_count = method_count

    # Overriding the info method to print the program file statistics as well
    def info(self):
        super().info() # Calling the superclass method
        print(f"Class count: {self.class_count}")
        print(f"Method count: {self.method_count}")

# Defining a class for the folder monitor
class FolderMonitor:
    # Initializing the folder monitor object with folder path and snapshot time
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.snapshot = time.time() # Setting the initial snapshot time to the current time
        self.files = {} # Creating an empty dictionary to store file objects

    # Defining a method to create file objects from the folder contents and store them in a dictionary
    def create_files(self):
        self.files = {} # Creating an empty dictionary to store file objects
        for filename in os.listdir(self.folder_path): # Iterating over each file in the folder path
            filepath = os.path.join(self.folder_path,filename) # Joining the folder path and file name to get the full path of the file
            name, extension = os.path.splitext(filename) # Splitting the file name and extension using os.path.splitext function
            created = os.path.getctime(filepath) # Getting the creation time of the file using os.path.getctime function
            updated = os.path.getmtime(filepath) # Getting the modification time of the file using os.path.getmtime function

            if extension in [".png", ".jpg"]: # Checking if the file is an image file by its extension
                size = f"{os.path.getsize(filepath)} bytes" # Getting the size of the file in bytes using os.path.getsize function 
                file_object = ImageFile(name,
                extension,
                created,
                updated,
                size) # Creating an image file object with name,


            elif extension == ".txt": # Checking if the file is a text file by its extension 
                with open(filepath,"r") as f: # Opening the file in read mode 
                    content = f.read() # Reading the content of the file 
                    line_count = len(content.split("\n")) # Counting the number of lines by splitting the content by newline character
                    word_count = len(content.split()) # Counting the number of words by splitting the content by whitespace characters
                    char_count = len(content) # Counting the number of characters by taking the length of the content
                file_object = TextFile(name, extension, created, updated, line_count, word_count, char_count) # Creating a text file object with name,

            elif extension in [".py", ".java"]: # Checking if the file is a program file by its extension
                with open(filepath,"r") as f: # Opening the file in read mode 
                    content = f.read() # Reading the content of the file 
                    line_count = len(content.split("\n")) # Counting the number of lines by splitting the content by newline character
                    class_count = content.count("class") # Counting the number of classes by finding the occurrence of "class" keyword in the content
                    method_count = content.count("def") + content.count("public") + content.count("private") # Counting the number of methods by finding the occurrence of "def", "public" and "private" keywords in the content
                file_object = ProgramFile(name, extension, created, updated, class_count, method_count) # Creating a program file object with name,
            else: # If the file is none of the above types, create a generic file object
                file_object = File(name, extension, created, updated) # Creating a file object with name, extension, created and updated attributes

            self.files[filename] = file_object # Storing the file object in the dictionary with filename as the key

    # Defining a method to update the snapshot time to the current time
    def commit(self):
        self.snapshot = time.time() # Setting the snapshot time to the current time
        print(f"Created Snapshot at: {time.ctime(self.snapshot)}") # Printing the snapshot time in a human-readable format using time.ctime function

    # Defining a method to print information about a given file name
    def info(self, filename):
        if filename in self.files: # Checking if the filename exists in the dictionary
            self.files[filename].info() # Calling the info method of the corresponding file object
        else:
            print(f"No such file: {filename}") # Printing an error message if the filename does not exist

    # Defining a method to print the status of each file in the folder since the last snapshot
    def status(self):
        for filename in self.files: # Iterating over each filename in the dictionary
            if self.files[filename].has_changed(self.snapshot): # Checking if the file has changed since the last snapshot using has_changed method
                print(f"{filename} - Changed") # Printing that the file has changed
            else:
                print(f"{filename} - No Change") # Printing that the file has not changed

    # Defining a method to detect and print any changes in files (addition or deletion) since the last snapshot
    def detect_changes(self):
        current_files = set(os.listdir(self.folder_path)) # Getting a set of current files in the folder path using os.listdir function
        previous_files = set(self.files.keys()) # Getting a set of previous files from the dictionary keys
        added_files = current_files - previous_files # Getting a set of added files by subtracting previous files from current files
        deleted_files = previous_files - current_files # Getting a set of deleted files by subtracting current files from previous files

        for filename in added_files: # Iterating over each filename in added files set
            print(f"{filename} - New File") # Printing that the file is new

        for filename in deleted_files: # Iterating over each filename in deleted files set
            print(f"{filename} - Deleted") # Printing that the file is deleted

        if added_files or deleted_files: # Checking if there are any changes in files 
            self.status() # Calling status method to print status of each file 
            self.commit() # Calling commit method to update snapshot time 

    # Defining a method to run a scheduled detection program every 5 seconds and print any changes to the console
    def run_scheduler(self):
        while True: # Creating an infinite loop 
            self.create_files() # Calling create_files method to update the dictionary with current files 
            self.detect_changes() # Calling detect_changes method to print any changes in files 
            time.sleep(5) # Pausing the execution for 5 seconds using time.sleep function

# Creating a folder monitor object with a hardcoded folder path (can be changed as per requirement)
folder_monitor = FolderMonitor("E:\programs\OOP Labs\Laboratory-works-OOP\control")
folder_monitor.create_files() # Creating file objects from the folder contents
folder_monitor.status() # Printing the status of each file

# Creating a thread object for running scheduler as a separate thread
scheduler_thread = threading.Thread(target=folder_monitor.run_scheduler) # Passing the run_scheduler method of the folder_monitor object as the target argument of the Thread constructor
scheduler_thread.start() # Starting the thread by calling the start method of the thread object
while True:
    command = input("> ")
    if command == "list":
        folder_monitor.create_files()
    elif command == "status":
        folder_monitor.status()
    elif command.startswith("info "):
        _, filename = command.split(" ", 1)
        folder_monitor.info(filename)
    elif command == "snapshot":
        folder_monitor.commit()
    elif command == "exit":
        break  # Exit the loop to terminate the program
    else:
        print("Invalid command. Available commands: list, status, info <filename>, snapshot, exit")
