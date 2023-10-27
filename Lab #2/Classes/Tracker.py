import os
import hashlib
import time
from datetime import datetime

class File:
    def __init__(self, name, created, updated):
        self.name = name
        self.created = created
        self.updated = updated
        self.changed = False

    def info(self):
        return f"{self.name} ({self.get_pretty_extension()}) - Created: {self.created}, Updated: {self.updated}"

    def get_pretty_extension(self):
        return ""

class TextFile(File):
    def __init__(self, name, created, updated, lines):
        super().__init__(name, created, updated)
        self.lines = lines
        self.word_count = len([word for line in lines for word in line.split()])
        self.char_count = sum(len(line) for line in lines)

    def info(self):
        return f"{super().info()}, Lines: {len(self.lines)}, Words: {self.word_count}, Characters: {self.char_count}"

    def get_pretty_extension(self):
        return "txt"

class ImageFile(File):
    def __init__(self, name, created, updated, size):
        super().__init__(name, created, updated)
        self.size = size

    def info(self):
        return f"{super().info()}, Size: {self.size[0]}x{self.size[1]}"

    def get_pretty_extension(self):
        return "png" if self.name.endswith(".png") else "jpg"

class ProgramFile(File):
    def __init__(self, name, created, updated, lines):
        super().__init__(name, created, updated)
        self.lines = lines
        self.class_count = len([line for line in lines if line.strip().startswith("class ")])
        self.method_count = len([line for line in lines if line.strip().startswith("def ")])

    def info(self):
        return f"{super().info()}, Lines: {len(self.lines)}, Classes: {self.class_count}, Methods: {self.method_count}"

    def get_pretty_extension(self):
        return "py" if self.name.endswith(".py") else "java"

class FolderSnapshot:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = self.get_files()
        self.snapshot_time = time.time()  # Initialize snapshot_time to current time
    
    def get_files(self):
        files = []
        for root, _, filenames in os.walk(self.folder_path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                created = os.path.getctime(filepath)
                updated = os.path.getmtime(filepath)
                with open(filepath, "r") as f:
                    lines = f.readlines()
                if filename.endswith(".txt"):
                    file = TextFile(filename, created, updated, lines)
                elif filename.endswith(".png") or filename.endswith(".jpg"):
                    size = (0, 0)
                    with open(filepath, "rb") as f:
                        data = f.read(24)
                        if data.startswith(b'\x89PNG\r\n\x1a\n'):
                            size = struct.unpack('>ii', data[16:24])
                        elif data.startswith(b'\xff\xd8'):
                            f.seek(0)
                            f.read(2)
                            b = f.read(1)
                            while b and ord(b) != 0xDA:
                                while ord(b) != 0xFF:
                                    b = f.read(1)
                                while ord(b) == 0xFF:
                                    b = f.read(1)
                                if 0xC0 <= ord(b) <= 0xC3:
                                    f.read(3)
                                    h, w = struct.unpack('>HH', f.read(4))
                                    size = (w, h)
                                    break
                                else:
                                    f.read(int.from_bytes(f.read(2), byteorder='big') - 2)
                                b = f.read(1)
                    file = ImageFile(filename, created, updated, size)
                elif filename.endswith(".py") or filename.endswith(".java"):
                    file = ProgramFile(filename, created, updated, lines)
                else:
                    file = File(filename, created, updated)
                files.append(file)
        return files
    
    def compare_snapshot(self):
        current_files = self.get_files()
        for file in self.files:
            current_file = next((f for f in current_files if f.name == file.name), None)
            if current_file is None:
                print(f"{file.name} - Removed")
                file.changed = True
            elif current_file.updated > self.snapshot_time:
                print(f"{file.name} - Changed")
                file.changed = True
            else:
                print(f"{file.name} - No Change")
                file.changed = False
        self.files = current_files
        self.snapshot_time = time.time()
    
    def info(self, filename):
        file = next((f for f in self.files if f.name == filename), None)
        if file is None:
            print(f"{filename} not found.")
        else:
            print(file.info())
    
    def status(self):
        for file in self.files:
            if file.changed:
                print(f"{file.name} - Changed")
            else:
                print(f"{file.name} - No Change")

if __name__ == "__main__":
    folder_path = "E:\programs\OOP Labs\Laboratory-works-OOP\control"
    folder_snapshot = FolderSnapshot(folder_path)
    
    folder_thread = threading.Thread(target=folder_snapshot.compare_snapshot)
    folder_thread.daemon = True  # Allow the thread to exit when the main program exits.
    folder_thread.start()
    
    while True:
        command = input("Enter a command (commit, info <filename>, status): ")
        if command == "commit":
            folder_snapshot.snapshot_time = time.time()
            print("Snapshot updated.")
        elif command.startswith("info "):
            filename = command.split()[1]
            folder_snapshot.info(filename)
        elif command == "status":
            folder_snapshot.status()
        else:
            print("Invalid command.")