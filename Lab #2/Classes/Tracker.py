import os
import datetime

class FileSnapshot:
    def __init__(self, filename, extension):
        self.filename = filename
        self.extension = extension
        self.created_time = datetime.datetime.now()
        self.updated_time = self.created_time

    def update_snapshot(self):
        self.updated_time = datetime.datetime.now()

class TextFileSnapshot(FileSnapshot):
    def __init__(self, filename):
        super().__init__(filename, "txt")
        self.line_count = 0
        self.word_count = 0
        self.character_count = 0

class ImageFileSnapshot(FileSnapshot):
    def __init__(self, filename):
        super().__init__(filename, "png")
        self.image_size = (0, 0)

class ProgramFileSnapshot(FileSnapshot):
    def __init__(self, filename):
        super().__init__(filename, "py")
        self.line_count = 0
        self.class_count = 0
        self.method_count = 0

class FileMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_snapshots = {}
        self.snapshot_time = None

    def commit(self):
        self.snapshot_time = datetime.datetime.now()

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".py"):
                with open(os.path.join(self.folder_path, filename), "r") as file:
                    lines = file.readlines()
                    snapshot = FileSnapshot(filename, "py")  # Create a FileSnapshot instance
                    snapshot.updated_time = datetime.datetime.now()
                    snapshot.line_count = len(lines)
                    snapshot.class_count = sum(1 for line in lines if "class" in line)
                    snapshot.method_count = sum(1 for line in lines if "def" in line)
                    self.file_snapshots[filename] = snapshot

    def info(self, filename):
        if filename in self.file_snapshots:
            file_snapshot = self.file_snapshots[filename]
            print(f"{file_snapshot.filename}.{file_snapshot.extension}")
            if file_snapshot.extension == "txt":
                print(f"Line Count: {file_snapshot.line_count}")
                print(f"Word Count: {file_snapshot.word_count}")
                print(f"Character Count: {file_snapshot.character_count}")
            elif file_snapshot.extension == "png":
                print(f"Image Size: {file_snapshot.image_size[0]}x{file_snapshot.image_size[1]}")
            elif file_snapshot.extension == "py":
                print(f"Line Count: {file_snapshot.line_count}")
                print(f"Class Count: {file_snapshot.class_count}")
                print(f"Method Count: {file_snapshot.method_count}")
            print(f"Created at: {file_snapshot.created_time}")
            print(f"Last Updated at: {file_snapshot.updated_time}")
        else:
            print(f"File not found: {filename}")

    def status(self):
        if self.snapshot_time is None:
            print("Snapshot not taken. Please commit a snapshot first.")
        else:
            for filename, file_snapshot in self.file_snapshots.items():
                status = "No Change" if file_snapshot.updated_time is not None and file_snapshot.updated_time <= self.snapshot_time else "Changed"
                print(f"{filename}: {status}")

    def update_snapshots(self):
        current_files = os.listdir(self.folder_path)
        for filename in current_files:
            if filename not in self.file_snapshots:
                file_extension = filename.split('.')[-1]
                if file_extension == "txt":
                    self.file_snapshots[filename] = TextFileSnapshot(filename)
                elif file_extension == "png":
                    self.file_snapshots[filename] = ImageFileSnapshot(filename)
                elif file_extension == "py":
                    self.file_snapshots[filename] = ProgramFileSnapshot(filename)
                else:
                    self.file_snapshots[filename] = FileSnapshot(filename, file_extension)

            if filename.endswith(".txt"):
                with open(os.path.join(self.folder_path, filename), "r") as file:
                    self.file_snapshots[filename].line_count = len(file.readlines())
                    file.seek(0)
                    self.file_snapshots[filename].word_count = len(file.read().split())
                    file.seek(0)
                    self.file_snapshots[filename].character_count = len(file.read())

            if filename.endswith(".png"):
                image_path = os.path.join(self.folder_path, filename)
                image_size = os.path.getsize(image_path)
                self.file_snapshots[filename].image_size = (image_size, image_size)

            if filename.endswith(".py"):
                with open(os.path.join(self.folder_path, filename), "r") as file:
                    lines = file.readlines()
                    self.file_snapshots[filename].line_count = len(lines)
                    self.file_snapshots[filename].class_count = sum(1 for line in lines if "class" in line)
                    self.file_snapshots[filename].method_count = sum(1 for line in lines if "def" in line)

class Main:
    def __init__(self, path):
        self.path = path

    def run(self):
        file_monitor = FileMonitor(self.path)

        while True:
            command = input("Enter a command (commit/info <filename>/status/exit): ").split()

            if command[0] == "commit":
                file_monitor.commit()
                print("Snapshot updated.")
            elif command[0] == "info":
                if len(command) == 2:
                    file_monitor.info(command[1])
            elif command[0] == "status":
                file_monitor.update_snapshots()
                file_monitor.status()
            elif command[0] == "exit":
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    main = Main("E:\programs\OOP Labs\Laboratory-works-OOP\control")
    main.run()