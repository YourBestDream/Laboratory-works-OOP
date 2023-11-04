import os
import struct
import hashlib
from datetime import datetime

class Document:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.last_modified_time = os.path.getmtime(filepath)
        self.snapshot_hash = self.calculate_hash()

    def calculate_hash(self):
        with open(self.filepath, 'rb') as file:
            return hashlib.md5(file.read()).hexdigest()

    def has_changed(self):
        current_hash = self.calculate_hash()
        return current_hash != self.snapshot_hash

    def update_snapshot(self):
        self.snapshot_hash = self.calculate_hash()

    def info(self):
        created_time = datetime.fromtimestamp(os.path.getctime(self.filepath))
        updated_time = datetime.fromtimestamp(os.path.getmtime(self.filepath))
        return {
            "Filename": self.filename,
            "Extension": os.path.splitext(self.filename)[1],
            "Created": created_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Updated": updated_time.strftime('%Y-%m-%d %H:%M:%S')
        }

# Override + Polymorphidm
class ImageDocument(Document):
    def get_png_dimensions(self):
        with open(self.filepath, 'rb') as img_file:
            img_file.seek(16)
            width, height = struct.unpack('>ii', img_file.read(8))
            return width, height

    def get_jpeg_dimensions(self):
        with open(self.filepath, 'rb') as img_file:
            img_file.read(2)
            b = img_file.read(1)
            try:
                while b and ord(b) != 0xDA:
                    while ord(b) != 0xFF: b = img_file.read(1)
                    while ord(b) == 0xFF: b = img_file.read(1)
                    if 0xC0 <= ord(b) <= 0xC3:
                        img_file.read(3)
                        h, w = struct.unpack('>HH', img_file.read(4))
                        return w, h
                    else:
                        img_file.read(int(struct.unpack('>H', img_file.read(2))[0]) - 2)
                    b = img_file.read(1)
                return None
            except struct.error:
                return None

    def get_dimensions(self):
        if self.filepath.lower().endswith('.png'):
            return self.get_png_dimensions()
        elif self.filepath.lower().endswith('.jpg') or self.filepath.lower().endswith('.jpeg'):
            return self.get_jpeg_dimensions()
        else:
            return None  # Placeholder for other image formats

    def info(self):
        base_info = super().info()
        dimensions = self.get_dimensions()
        if dimensions:
            base_info["Dimensions"] = f"{dimensions[0]}x{dimensions[1]}"
        else:
            base_info["Dimensions"] = "Unknown"
        return base_info

class TextDocument(Document):
    def info(self):
        base_info = super().info()
        with open(self.filepath, 'r') as file:
            content = file.read()
            base_info["Line Count"] = len(content.splitlines())
            base_info["Word Count"] = len(content.split())
            base_info["Character Count"] = len(content)
        return base_info

class ProgramDocument(Document):
    def info(self):
        base_info = super().info()
        with open(self.filepath, 'r') as file:
            content = file.readlines()
            base_info["Line Count"] = len(content)
            base_info["Class Count"] = sum(1 for line in content if 'class ' in line)
            base_info["Method Count"] = sum(1 for line in content if 'def ' in line)
        return base_info