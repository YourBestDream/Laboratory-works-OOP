import hashlib
import os
import struct
import time


class File:
    def __init__(self, name, created, updated):
        self.name = name
        self.created = created
        self.updated = updated
        self.hash = self.get_hash()
        self.changed = False

    def info(self):
        return f"Name: {self.name}, Created: {self.created}, Updated: {self.updated}, Hash: {self.hash}, Changed: {self.changed}"

    def get_hash(self):
        return hashlib.md5(self.name.encode() + str(self.created).encode() + str(self.updated).encode()).hexdigest()


class TextFile(File):
    def __init__(self, name, created, updated, lines, folder_path):
        super().__init__(name, created, updated)
        self.lines = lines
        self.word_count = len([word for line in lines for word in line.split()])
        self.char_count = sum(len(line) for line in lines)
        self.folder_path = folder_path

    def info(self):
        return f"{super().info()}, Lines: {len(self.lines)}, Words: {self.word_count}, Characters: {self.char_count}"

    def get_pretty_extension(self):
        return "txt"

    def get_path(self):
        return os.path.join(self.folder_path, self.name)

    def update(self):
        current_updated = os.path.getmtime(self.get_path())
        if current_updated > self.updated:
            self.updated = current_updated
            self.changed = True
        else:
            self.changed = False

    def get_selection(self, start_line, end_line):
        selection = ""
        for i in range(start_line, end_line + 1):
            selection += self.lines[i]
        return selection


class ImageFile(File):
    def __init__(self, name, created, updated, size):
        super().__init__(name, created, updated)
        self.size = size

    def info(self):
        return f"{super().info()}, Size: {self.size[0]}x{self.size[1]}"

    def get_pretty_extension(self):
        return "img"


class ProgramFile(TextFile):
    def __init__(self, name, created, updated, lines, folder_path):
        super().__init__(name, created, updated, lines, folder_path)

    def get_pretty_extension(self):
        return "code"


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
                if os.path.exists(filepath):
                    created = os.path.getctime(filepath)
                    updated = os.path.getmtime(filepath)
                    with open(filepath, "r") as f:
                        lines = f.readlines()
                    if filename.endswith(".txt"):
                        file = TextFile(filename, created, updated, lines, self.folder_path)
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
                        file = ProgramFile(filename, created, updated, lines, self.folder_path)
                    else:
                        file = File(filename, created, updated)
                    if file not in files:
                        files.append(file)
                        print(f"{file.name} - Created")
                else:
                    print(f"{filename} - Deleted")
        return files

    def info(self, filename):
        for file in self.files:
            if file.name == filename:
                print(file.info())
                return
        print(f"File {filename} not found.")

    def status(self):
        for file in self.files:
            if isinstance(file, TextFile):
                if os.path.exists(file.get_path()):
                    file.update()
                    if file.changed:
                        print(f"{file.name} - Changed")
                    else:
                        print(f"{file.name} - No Change")
                else:
                    print(f"{file.name} - Deleted")
            else:
                print(f"{file.name} - No Change")

    def get_selection(self, filename, start_line, end_line):
        for file in self.files:
            if isinstance(file, TextFile) and file.name == filename:
                return file.get_selection(start_line, end_line)
        return ""


if __name__ == "__main__":
    folder_path = "E:\programs\OOP Labs\Laboratory-works-OOP\control"
    folder_snapshot = FolderSnapshot(folder_path)
    
    while True:
        command = input("Enter a command (commit, info <filename>, status, selection <filename> <start_line> <end_line>): ")
        if command == "commit":
            folder_snapshot.snapshot_time = time.time()
            print("Snapshot updated.")
        elif command.startswith("info "):
            filename = command.split()[1]
            folder_snapshot.info(filename)
        elif command == "status":
            folder_snapshot.status()
        elif command.startswith("selection "):
            args = command.split()
            if len(args) == 4:
                filename = args[1]
                start_line = int(args[2])
                end_line = int(args[3])
                selection = folder_snapshot.get_selection(filename, start_line, end_line)
                print(selection)
            else:
                print("Invalid command.")
        else:
            print("Invalid command.")