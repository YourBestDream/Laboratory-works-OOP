from .FolderMonitor import FolderMonitor

class Main:
    from .FolderMonitor import FolderMonitor

class Main:
    def __init__(self, path):
        self.path = path
        self.monitor = FolderMonitor(self.path)
        self.monitor.start_monitoring()  # Start the monitoring thread

    def run(self):
        print("Folder Monitoring System")
        print("Commands:")
        print("  commit - Update the snapshot to the current state.")
        print("  info <filename> - Display information about a specific file.")
        print("  status - Display the status of all files compared to the last snapshot.")
        print("  exit - Exit the monitoring system.")
        print()
        
        while True:
            command = input("Enter command: ").strip()
            
            if command == "exit":
                print("Exiting Folder Monitoring System.")
                break
            else:
                response = self.monitor.execute_command(command)
                if isinstance(response, dict):
                    for key, value in response.items():
                        if isinstance(value, dict):
                            print(key)
                            for k, v in value.items():
                                print(f"  {k}: {v}")
                        else:
                            print(f"{key} - {value}")
                else:
                    print(response)
                print()