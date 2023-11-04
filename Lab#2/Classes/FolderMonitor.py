import os
import threading
import time
from datetime import datetime
from .Documents import Document, ImageDocument, TextDocument, ProgramDocument

class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.documents = self.initialize_documents()
        self.snapshot_time = datetime.now()
        self.reported_changes = set()

    def initialize_documents(self):
        documents = {}
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1]
                if ext in ['.png', '.jpg']:
                    doc = ImageDocument(filepath)
                elif ext in ['.txt']:
                    doc = TextDocument(filepath)
                elif ext in ['.py', '.java']:
                    doc = ProgramDocument(filepath)
                else:
                    doc = Document(filepath)
                documents[filename] = doc
        return documents

    def commit(self):
        self.snapshot_time = datetime.now()
        filenames_to_remove = []
        for filename, doc in self.documents.items():
            if os.path.exists(doc.filepath):
                doc.update_snapshot()
            else:
                filenames_to_remove.append(filename)
        
        for filename in filenames_to_remove:
            del self.documents[filename]

        for filename in os.listdir(self.folder_path):
            if filename not in self.documents:
                filepath = os.path.join(self.folder_path, filename)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(filename)[1]
                    if ext in ['.png', '.jpg']:
                        doc = ImageDocument(filepath)
                    elif ext in ['.txt']:
                        doc = TextDocument(filepath)
                    elif ext in ['.py', '.java']:
                        doc = ProgramDocument(filepath)
                    else:
                        doc = Document(filepath)
                    self.documents[filename] = doc
        self.reported_changes.clear()

    def get_document_info(self, filename):
        if filename in self.documents:
            return self.documents[filename].info()
        return None

    def get_status(self):
        status = {}
        current_files = set(os.listdir(self.folder_path))

        for filename in self.documents:
            if filename not in current_files:
                status[filename] = "Deleted"
            else:
                status[filename] = "Changed" if self.documents[filename].has_changed() else "No Changes"

        for filename in current_files:
            if filename not in self.documents:
                status[filename] = "New File"

        return status

    def execute_command(self, command):
        if command == "commit":
            self.commit()
            return "Snapshot updated."
        
        if command.startswith("info"):
            _, filename = command.split()
            info = self.get_document_info(filename)
            return info if info else f"{filename} not found."
        
        if command == "status":
            return self.get_status()
        
        return "Invalid command."

    def check_for_changes(self):
        status = self.get_status()
        for filename, change in status.items():
            if change != "No Changes" and filename not in self.reported_changes:
                print(f"\n{filename}: {change}")
                self.reported_changes.add(filename)

    # Monitoring in separate thread
    def start_monitoring(self):
        def monitor():
            while True:
                self.check_for_changes()
                time.sleep(5)
        monitoring_thread = threading.Thread(target=monitor, daemon=True)
        monitoring_thread.start()