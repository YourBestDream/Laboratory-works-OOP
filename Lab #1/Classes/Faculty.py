from .Study_Field import StudyField
from .Student import Student

class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.graduates = []
        self.study_field = study_field

    def add_student(self, student):
        self.students.append(student)

    def graduate_student(self, student):
        if student in self.students:
            self.students.remove(student)
            self.graduates.append(student)
            student.graduate = True
    
    def add_graduated_student(self, student):
        self.graduates.append(student)

    def to_string(self):
        return f"{self.name},{self.abbreviation},{self.study_field}"

    @staticmethod
    def from_string(string):
        fields = string.split(',')
        study_field_name = fields[2].split('.')[1]  # Access the name as a string
        study_field = StudyField[study_field_name]  # Access the enum value by name
        return Faculty(fields[0], fields[1], study_field)