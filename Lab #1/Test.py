from enum import Enum
from datetime import date

#Пермести все функции в классы
#Имплемментируй кейсы менб в качестве методов класса скорее всего menu

class StudyField(Enum):
    MECHANICAL_ENGINEERING = 1
    SOFTWARE_ENGINEERING = 2
    FOOD_TECHNOLOGY = 3
    URBANISM_ARCHITECTURE = 4
    VETERINARY_MEDICINE = 5

class Student:
    def __init__(self, firstName, lastName, email, idnum, facultyAbbreviation, enrollmentDate, dateOfBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.idnum = idnum
        self.facultyAbbreviation = facultyAbbreviation
        self.enrollmentDate = enrollmentDate
        self.dateOfBirth = dateOfBirth

    def to_string(self):
        return f"{self.firstName},{self.lastName},{self.email},{self.idnum},{self.facultyAbbreviation},{self.enrollmentDate},{self.dateOfBirth}"

    @staticmethod
    def from_string(string):
        fields = string.split(',')
        return Student(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6])

class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.study_field = study_field

    def add_student(self, student):
        self.students.append(student)

    def graduate_student(self, student):
        if student in self.students:
            self.students.remove(student)

    def to_string(self):
        return f"{self.name},{self.abbreviation},{self.study_field}"

    @staticmethod
    def from_string(string):
        fields = string.split(',')
        study_field_name = fields[2].split('.')[1]  # Access the name as a string
        study_field = StudyField[study_field_name]  # Access the enum value by name
        return Faculty(fields[0], fields[1], study_field)

class FileManager:
    def __init__(self):
        self.faculty_file = "faculties.txt"
        self.students_file = "students.txt"

    def save_data(self, faculties):
        with open(self.faculty_file, "w") as file:
            for faculty in faculties:
                file.write(faculty.to_string() + "\n")
                for student in faculty.students:
                    file.write(student.to_string() + "\n")

    def load_data(self):
        faculties = []
        try:
            with open(self.faculty_file, "r") as file:
                lines = file.read().splitlines()
                while lines:
                    faculty_data = lines.pop(0).split(',')
                    faculty = Faculty.from_string(','.join(faculty_data))
                    while lines and not lines[0].startswith(","):
                        student_data = lines.pop(0)
                        student = Student.from_string(student_data)
                        faculty.add_student(student)
                    faculties.append(faculty)
        except FileNotFoundError:
            pass
        return faculties

file_manager = FileManager()
faculties = file_manager.load_data()

def create_faculty():
    name = input("Enter faculty name: ")
    abbreviation = input("Enter faculty abbreviation: ")
    field = input("Enter faculty field (e.g., MECHANICAL_ENGINEERING): ")
    study_field = StudyField[field]
    faculty = Faculty(name, abbreviation, study_field)
    faculties.append(faculty)
    print(f"Faculty '{name}' created successfully.")

def assign_student_to_faculty():
    name = input("Enter student first name: ")
    surname = input("Enter student last name: ")
    email = input("Enter student email: ")
    faculty_abbreviation = input("Enter faculty abbreviation: ")
    for faculty in faculties:
        if faculty.abbreviation == faculty_abbreviation:
            if len(faculty.students) == 0:
                idnum = 1
            else:
                idnum = len(faculty.students) + 1
    enrollment = input("Student's enrollment date (YYYY-MM-DD): ")
    birth = input("Student's date of birth (YYYY-MM-DD): ")
    student = Student(name, surname, email, faculty_abbreviation, idnum, enrollment, birth)
    for faculty in faculties:
        if faculty.abbreviation == faculty_abbreviation:
            faculty.add_student(student)
            print(f"Student '{name} {surname}' assigned to faculty '{faculty.name}'.")

def graduate_student_from_faculty():
    email = input("Enter student email: ")
    faculty_abbreviation = input("Enter faculty abbreviation: ")
    student = find_student_by_email(email)
    faculty = find_faculty_by_abbreviation(faculty_abbreviation)
    if student and faculty:
        faculty.graduate_student(student)
        print(f"Student '{student.firstName} {student.lastName}' graduated from faculty '{faculty.name}'.")

def display_enrolled_students():
    faculty_abbreviation = input("Enter faculty abbreviation: ")
    faculty = find_faculty_by_abbreviation(faculty_abbreviation)
    if faculty:
        print(f"Currently enrolled students in faculty '{faculty.name}':")
        for student in faculty.students:
            print(f"{student.firstName} {student.lastName} ({student.email})")

def display_graduates():
    faculty_abbreviation = input("Enter faculty abbreviation: ")
    faculty = find_faculty_by_abbreviation(faculty_abbreviation)
    if faculty:
        print(f"Graduates from faculty '{faculty.name}':")
        all_students = find_all_students()
        graduates = [student for student in all_students if student not in faculty.students]
        for student in graduates:
            print(f"{student.firstName} {student.lastName} ({student.email})")

def check_student_belonging():
    email = input("Enter student email: ")
    faculty_abbreviation = input("Enter faculty abbreviation: ")
    student = find_student_by_email(email)
    faculty = find_faculty_by_abbreviation(faculty_abbreviation)
    if student and faculty:
        if student in faculty.students:
            print(f"Student '{student.firstName} {student.lastName}' belongs to faculty '{faculty.name}'.")
        else:
            print(f"Student '{student.firstName} {student.lastName}' does not belong to faculty '{faculty.name}'.")

def find_student_by_email(email):
    for faculty in faculties:
        for student in faculty.students:
            if student.email == email:
                return student
    print(f"Student with email '{email}' not found.")
    return None

def find_faculty_by_abbreviation(abbreviation):
    for faculty in faculties:
        if faculty.abbreviation == abbreviation:
            return faculty
    print(f"Faculty with abbreviation '{abbreviation}' not found.")
    return None

def find_all_students():
    all_students = []
    for faculty in faculties:
        all_students.extend(faculty.students)
    return all_students

while True:
    print("\nUniversity Management System")
    print("1. Faculty Operations")
    print("2. General Operations")
    print("3. Exit")
    choice = input("Enter your choice: ")

    match choice:
        case '1':
            while True:
                print("\nFaculty Operations")
                print("1. Create and assign a student to a faculty")
                print("2. Graduate a student from a faculty")
                print("3. Display current enrolled students")
                print("4. Display graduates")
                print("5. Check if a student belongs to this faculty")
                print("\n6. Back to main menu")
                print("7. Exit the program")
                faculty_choice = input("Enter your choice: ")

                match faculty_choice:
                    case '1':
                        assign_student_to_faculty()
                    case '2':
                        graduate_student_from_faculty()
                    case '3':
                        display_enrolled_students()
                    case '4':
                        display_graduates()
                    case '5':
                        check_student_belonging()
                    case '6':
                        break
                    case '7':
                        print("Exiting program. Goodbye!")
                        file_manager.save_data(faculties)
                        exit()
                    case _:
                        print("Invalid choice.")
        case '2':
            while True:
                print("\nGeneral Operations")
                print("1. Create a new faculty")
                print("2. Search what faculty a student belongs to by email")
                print("3. Display University faculties")
                print("4. Display all faculties belonging to a field")
                print("\n5. Back to main menu")
                print("6. Exit the program")
                general_choice = input("Enter your choice: ")

                match general_choice:
                    case '1':
                        create_faculty()
                    case '2':
                        email = input("Enter student email: ")
                        student = find_student_by_email(email)
                        if student:
                            for faculty in faculties:
                                if student in faculty.students:
                                    print(f"Student '{student.firstName} {student.lastName}' belongs to faculty '{faculty.name}'.")
                                    break
                            else:
                                print(f"Student '{student.firstName} {student.lastName}' does not belong to any faculty.")
                    case '3':
                        print("\nUniversity Faculties:")
                        for faculty in faculties:
                            print(f"{faculty.name} ({faculty.abbreviation})")

                    case '4':
                        field = input("Enter study field (e.g., MECHANICAL_ENGINEERING): ")
                        study_field = StudyField[field]
                        print(f"\nFaculties in the '{field}' field:")
                        for faculty in faculties:
                            if faculty.study_field == study_field:
                                print(f"{faculty.name} ({faculty.abbreviation})")

                    case '5':
                        break
                    
                    case '6':
                        print("Exiting program. Goodbye!")
                        file_manager.save_data(faculties)
                        exit()
                    case _:
                        print("Invalid choice.")
        case '3':
            print("Exiting program. Goodbye!")
            file_manager.save_data(faculties)
            break
        case _:
            print("Invalid choice.")