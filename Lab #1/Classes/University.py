from .File_Manager import FileManager
from .Faculty import Faculty
from .Student import Student
from .Study_Field import StudyField

class University:
    def __init__(self):
        self.file_manager = FileManager()
        self.faculties = self.file_manager.load_faculties()
        self.students = self.file_manager.load_students()
        for faculty in self.faculties:
            for student in self.students:
                if (student.facultyAbbreviation == faculty.abbreviation and student.graduate != "True"):
                    faculty.add_student(student)
                else:
                    faculty.add_graduated_student(student)

    def create_faculty(self):
        name = input("Enter faculty name: ")
        abbreviation = input("Enter faculty abbreviation: ")
        field = input("Enter faculty field (e.g., MECHANICAL_ENGINEERING): ")
        study_field = StudyField[field]
        faculty = Faculty(name, abbreviation, study_field)
        self.faculties.append(faculty)
        print(f"Faculty '{name}' created successfully.")

    def assign_student_to_faculty(self):
        name = input("Enter student first name: ")
        surname = input("Enter student last name: ")
        email = input("Enter student email: ")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        for faculty in self.faculties:
            if faculty.abbreviation == faculty_abbreviation:
                if len(faculty.students) == 0:
                    idnum = 1
                else:
                    idnum = len(faculty.students) + 1
        enrollment = input("Student's enrollment date (YYYY-MM-DD): ")
        birth = input("Student's date of birth (YYYY-MM-DD): ")
        graduate = False
        student = Student(name, surname, email, idnum, faculty_abbreviation, enrollment, birth, graduate)
        for faculty in self.faculties:
            if faculty.abbreviation == faculty_abbreviation:
                faculty.add_student(student)
                self.students.append(student)  # Add student to the list of all students
                print(f"Student '{name} {surname}' assigned to faculty '{faculty.name}'.")

    def graduate_student_from_faculty(self):
        email = input("Enter student email: ")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        student = self.find_student_by_email(email)
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if student and faculty:
            faculty.graduate_student(student)
            print(f"Student '{student.firstName} {student.lastName}' graduated from faculty '{faculty.name}'.")

    def display_enrolled_students(self):
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if faculty:
            print(f"\nCurrently enrolled students in faculty '{faculty.name}':")
            for student in faculty.students:
                print(f"└─{student.firstName} {student.lastName} ({student.email})")

    def display_graduates(self):
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if faculty:
            print(f"\nGraduates from faculty '{faculty.name}':")
            all_students = self.find_all_students()
            graduates = faculty.graduates
            for student in graduates:
                print(f"└─{student.firstName} {student.lastName} ({student.email})")

    def check_student_belonging(self):
        email = input("Enter student email: ")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        student = self.find_student_by_email(email)
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if student and faculty:
            if student in faculty.students:
                print(f"\nStudent '{student.firstName} {student.lastName}' belongs to faculty '{faculty.name}'.")
            else:
                print(f"\nStudent '{student.firstName} {student.lastName}' does not belong to faculty '{faculty.name}'.")

    def find_student_by_email(self, email):
        for student in self.students:
            if student.email == email:
                return student
        print(f"\nStudent with email '{email}' not found.")
        return None

    def find_faculty_by_abbreviation(self, abbreviation):
        for faculty in self.faculties:
            if faculty.abbreviation == abbreviation:
                return faculty
        print(f"\nFaculty with abbreviation '{abbreviation}' not found.")
        return None

    def find_all_students(self):
        return self.students