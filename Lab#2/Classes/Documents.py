import os
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

class ImageDocument(Document):
    def info(self):
        base_info = super().info()
        # Here we're just providing a placeholder dimension as we aren't actually reading the image
        base_info["Dimensions"] = "Placeholder"
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