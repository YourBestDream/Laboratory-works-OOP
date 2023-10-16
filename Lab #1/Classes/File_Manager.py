from .Faculty import Faculty
from .Student import Student

#Saves won't work if you will delete info from files. You must delete both .txt in order to work with program as you please from the very beginning.

class FileManager:
    def __init__(self):
        self.faculties_file = "faculties.txt"
        self.students_file = "students.txt"

    def save_faculties(self, faculties):
        with open(self.faculties_file, "w", encoding="utf-8") as file:
            for faculty in faculties:
                file.write(faculty.to_string() + "\n")

    def save_students(self, students):
        with open(self.students_file, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_string() + "\n")

    def load_faculties(self):
        faculties = []
        try:
            with open(self.faculties_file, "r", encoding="utf-8") as file:
                lines = file.read().splitlines()
                for line in lines:
                    faculty = Faculty.from_string(line)
                    faculties.append(faculty)
        except FileNotFoundError:
            pass
        return faculties

    def load_students(self):
        students = []
        try:
            with open(self.students_file, "r") as file:
                lines = file.read().splitlines()
                for line in lines:
                    student = Student.from_string(line)
                    students.append(student)
        except FileNotFoundError:
            pass
        return students