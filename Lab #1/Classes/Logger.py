from datetime import datetime

class Logger():
    def __init__(self):
        self.logger_file = "logger.txt"

    def log(self, message):
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            with open(self.logger_file, "a", encoding="utf-8") as file:
                file.write(f"[{time}] {message}\n")
        except FileNotFoundError:
            with open(self.logger_file, "w", encoding="utf-8") as file:
                file.write(f"[{time}] {message}\n")