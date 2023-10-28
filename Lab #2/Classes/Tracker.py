import os
import hashlib
from datetime import datetime

class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.last_snapshot_hash = self.calculate_hash()
        self.snapshot_time = datetime.now()

    def calculate_hash(self):
        sha256 = hashlib.sha256()
        with open(self.path, 'rb') as file:
            while True:
                data = file.read(65536)  # Read in 64k chunks
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

    def has_changed(self):
        current_hash = self.calculate_hash()
        return current_hash != self.last_snapshot_hash

    def get_file_info(self):
        created_time = datetime.fromtimestamp(os.path.getctime(self.path))
        updated_time = datetime.fromtimestamp(os.path.getmtime(self.path))
        return f'{self.name} - Created: {created_time}, Updated: {updated_time}'

    def get_status(self):
        if self.has_changed():
            return f'{self.name} - Changed'
        else:
            return f'{self.name} - No Change'


class TextFile(File):
    def get_file_info(self):
        file_info = super().get_file_info()
        with open(self.path, 'r') as text_file:
            lines = text_file.readlines()
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
            return f'{file_info}, Lines: {len(lines)}, Words: {word_count}, Characters: {char_count}'


class ImageFile(File):
    def get_file_info(self):
        file_info = super().get_file_info()
        width, height = self.get_image_dimensions()
        return f'{file_info}, Image Size: {width}x{height}'

    def get_image_dimensions(self):
        # You can implement this to extract image dimensions from image files (png, jpg).
        return (0, 0)  # For example, return 0x0


class ProgramFile(File):
    def get_file_info(self):
        file_info = super().get_file_info()
        line_count, class_count, method_count = self.get_code_metrics()
        return f'{file_info}, Lines: {line_count}, Classes: {class_count}, Methods: {method_count}'

    def get_code_metrics(self):
        # You can implement this to count lines, classes, and methods in program files (.py, .java).
        return (0, 0, 0)  # For example, return (0, 0, 0)


class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = {}

    def commit(self):
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in self.files:
                    self.files[file_path] = File(file, file_path)
                else:
                    self.files[file_path].last_snapshot_hash = self.files[file_path].calculate_hash()
                    self.files[file_path].snapshot_time = datetime.now()

    def info(self, filename):
        if filename in self.files:
            file = self.files[filename]
            if filename.lower().endswith('.txt'):
                return TextFile(filename, file.path).get_file_info()
            elif filename.lower().endswith(('.png', '.jpg')):
                return ImageFile(filename, file.path).get_file_info()
            elif filename.lower().endswith(('.py', '.java')):
                return ProgramFile(filename, file.path).get_file_info()
            else:
                return file.get_file_info()
        else:
            return "File not found."

    def status(self):
        for filename, file in self.files.items():
            print(file.get_status())

if __name__ == "__main__":
    folder_path = "E:\programs\OOP Labs\Laboratory-works-OOP\control"
    monitor = FolderMonitor(folder_path)

    while True:
        command = input("Enter command (commit, info <filename>, status): ").split()
        if command[0] == "commit":
            monitor.commit()
        elif command[0] == "info":
            if len(command) == 2:
                filename = command[1]
                result = monitor.info(filename)
                print(result)
            else:
                print("Invalid command. Usage: info <filename>")
        elif command[0] == "status":
            monitor.status()
        else:
            print("Invalid command.")
