from .File_Manager import FileManager
from .Faculty import Faculty
from .Student import Student
from .Study_Field import StudyField
from .Logger import Logger

class University:
    def __init__(self):
        self.file_manager = FileManager()
        self.faculties = self.file_manager.load_faculties()
        self.students = self.file_manager.load_students()
        # self.graduates = [student for student in self.students if student.graduate == "True"]
        self.logger = Logger()
        for faculty in self.faculties:
            for student in self.students:
                if (student.facultyAbbreviation == faculty.abbreviation and student.graduate != "True"):
                    faculty.add_student(student)
                else:
                    faculty.add_graduated_student(student)

    def create_faculty(self):
        name = input("Enter faculty name: ")
        abbreviation = input("Enter faculty abbreviation: ")
        if self.find_faculty_by_abbreviation(abbreviation):
            print(f"Faculty with abbreviation '{abbreviation}' already exists.")
            return
        else:
            pass
        field = input("Enter faculty field (e.g., MECHANICAL_ENGINEERING): ")
        study_field = StudyField[field]
        if not study_field:
            print(f"Invalid study field '{field}'.")
            return
        faculty = Faculty(name, abbreviation, study_field)
        self.faculties.append(faculty)
        print(f"Faculty '{name}' created successfully.")
        self.logger.log(f"Faculty '{name}' created successfully.")

    def assign_student_to_faculty(self):
        name = input("Enter student first name: ")
        surname = input("Enter student last name: ")
        email = input("Enter student email: ")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        if not self.find_faculty_by_abbreviation(faculty_abbreviation):
            # print(f"Faculty with abbreviation '{faculty_abbreviation}' not found.")
            return
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
                self.logger.log(f"Student '{name} {surname} {email} ID = {idnum} {enrollment} {birth}' assigned to faculty '{faculty.name}'.")

    def batch_enrollment(self):
        with open("enrollment.txt", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            for line in lines:
                student = Student.from_string(line)
                for faculty in self.faculties:
                    if faculty.abbreviation == student.facultyAbbreviation:
                        faculty.add_student(student)
                        self.students.append(student)  # Add student to the list of all students
                        print(f"Student '{student.firstName} {student.lastName}' assigned to faculty '{student.facultyAbbreviation}'.")

    def graduate_student_from_faculty(self):
        email = input("Enter student email: ")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        student = self.find_student_by_email(email)
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if student and faculty:
            faculty.graduate_student(student)
            print(f"Student '{student.firstName} {student.lastName}' graduated from faculty '{faculty.name}'.")
            self.logger.log(f"Student '{student.firstName} {student.lastName} {student.email} ID = {student.idnum} {student.enrollmentDate} {student.dateOfBirth}' graduated from faculty '{faculty.name}'.")

    def student_match(self, student1, student2):
        return (
            student1.firstName == student2.firstName and
            student1.lastName == student2.lastName and
            student1.email == student2.email and
            student1.idnum == student2.idnum and
            student1.facultyAbbreviation == student2.facultyAbbreviation and
            student1.enrollmentDate == student2.enrollmentDate and
            student1.dateOfBirth == student2.dateOfBirth
        )

    def batch_graduation(self):
        with open("graduation.txt", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            for line in lines:
                student = Student.from_string(line)
                print(student.firstName, student.lastName)
                
                # Camparison of students by all fields except for the 'graduate' field
                matching_students = [s for s in self.students if self.student_match(student, s)]
                
                if matching_students:
                    faculty = self.find_faculty_by_abbreviation(student.facultyAbbreviation)
                    if student and faculty:
                        faculty.graduate_student(matching_students[0])  # Graduate the matching student
                        print(f"Student '{student.firstName} {student.lastName}' graduated from faculty '{student.facultyAbbreviation}'.")
                        self.logger.log(f"Student '{student.firstName} {student.lastName} {student.email} ID = {student.idnum} {student.enrollmentDate} {student.dateOfBirth}' graduated from faculty '{faculty.name}'.")
                else:
                    print("Students whom you're trying to graduate are not enrolled in any faculty.")

    def display_enrolled_students(self):
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if faculty:
            print(f"\nCurrently enrolled students in faculty '{faculty.name}':")
            self.logger.log(f"Currently enrolled students in faculty '{faculty.name}':")
            for student in faculty.students:
                print(f"└─{student.firstName} {student.lastName} ({student.email})")
                self.logger.log(f"└─{student.firstName} {student.lastName} ({student.email})")

    def display_graduates(self):
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        self.logger.log(f"Abbreviation '{faculty_abbreviation}':")
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if faculty:
            print(f"\nGraduates from faculty '{faculty.name}':")
            self.logger.log(f"Faculty '{faculty.name}':")
            all_students = self.find_all_students()
            graduates = faculty.graduates
            for student in graduates:
                print(f"└─{student.firstName} {student.lastName} ({student.email})")
                self.logger.log(f"└─{student.firstName} {student.lastName} ({student.email})")

    def check_student_belonging(self):
        email = input("Enter student email: ")
        self.logger.log(f"Email '{email}':")
        faculty_abbreviation = input("Enter faculty abbreviation: ")
        self.logger.log(f"Abbreviation '{faculty_abbreviation}':")
        student = self.find_student_by_email(email)
        faculty = self.find_faculty_by_abbreviation(faculty_abbreviation)
        if student and faculty:
            if student in faculty.students:
                print(f"\nStudent '{student.firstName} {student.lastName}' belongs to faculty '{faculty.name}'.")
                self.logger.log(f"Student '{student.firstName} {student.lastName} {student.email} ID = {student.idnum} {student.enrollmentDate} {student.dateOfBirth}' belongs to faculty '{faculty.name}'.")
            else:
                print(f"\nStudent '{student.firstName} {student.lastName}' does not belong to faculty '{faculty.name}'.")
                self.logger.log(f"Student '{student.firstName} {student.lastName} {student.email} ID = {student.idnum} {student.enrollmentDate} {student.dateOfBirth}' does not belong to faculty '{faculty.name}'.")


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