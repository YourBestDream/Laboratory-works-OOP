from .Logger import Logger
from .Study_Field import StudyField

class Menu:
    def __init__(self, university):
        self.university = university
        self.logger = Logger()
    def run(self):
        self.logger.log("Program started.")
        while True:
            print("\n" + "=" * 30)
            print(" University Management System")
            print("=" * 30)
            print("└─1. Faculty Operations")
            print("└─2. General Operations")
            print("\n  3. Exit")
            choice = input("Enter your choice: ")
            match choice:
                case '1':
                    self.run_faculty_operations()
                case '2':
                    self.run_general_operations()
                case '3':
                    print("Exiting program. Goodbye!")
                    self.logger.log("Program ended.\n")
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    break
                case _:
                    self.logger.log("Invalid choice.")
                    print("Invalid choice.")

    def run_faculty_operations(self):
        self.logger.log("User chose Faculty Operations.")
        while True:
            print("\n" + "=" * 30)
            print(" Faculty Operations")
            print("=" * 30)
            print("└─1. Create and assign a student to a faculty")
            print("└─2. Batch enrollment of students to a faculty")
            print("└─3. Graduate a student from a faculty")
            print("└─4. Batch graduation of students from a faculty")
            print("└─5. Display current enrolled students")
            print("└─6. Display graduates")
            print("└─7. Check if a student belongs to this faculty")
            print("\n  8. Back to the main menu")
            print("  9. Exit the program")
            faculty_choice = input("Enter your choice: ")
            self.logger.log(f"User chose '{faculty_choice}'.")
            match faculty_choice:
                case '1':
                    self.university.assign_student_to_faculty()
                case '2':
                    self.university.batch_enrollment()
                case '3':
                    self.university.graduate_student_from_faculty()
                case '4':
                    self.university.batch_graduation()
                case '5':
                    self.university.display_enrolled_students()
                case '6':
                    self.university.display_graduates()
                case '7':
                    self.university.check_student_belonging()
                case '8':
                    break
                case '9':
                    self.logger.log("Program ended.\n")
                    print("Exiting program. Goodbye!")
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    exit()
                case _:
                    self.logger.log("Invalid choice.")
                    print("Invalid choice.")

    def run_general_operations(self):
        self.logger.log("User chose Faculty Operations.")
        while True:
            print("\n" + "=" * 30)
            print(" General Operations")
            print("=" * 30)
            print("└─1. Create a new faculty")
            print("└─2. Search what faculty a student belongs to by email")
            print("└─3. Display University faculties")
            print("└─4. Display all faculties belonging to a field")
            print("\n  5. Back to the main menu")
            print("  6. Exit the program")
            general_choice = input("Enter your choice: ")
            self.logger.log(f"User chose '{general_choice}'.")
            match general_choice:
                case '1':
                    self.university.create_faculty()
                case '2':
                    email = input("Enter student email: ")
                    student = self.university.find_student_by_email(email)
                    if student:
                        for faculty in self.university.faculties:
                            if student in faculty.students:
                                print(f"Student '{student.firstName} {student.lastName}' belongs to faculty '{faculty.name}'.")
                                break
                        else:
                            print(f"Student '{student.firstName} {student.lastName}' does not belong to any faculty.")
                case '3':
                    print("\nUniversity Faculties:")
                    for faculty in self.university.faculties:
                        print(f"{faculty.name} ({faculty.abbreviation})")
                case '4':
                    field = input("Enter study field (e.g., MECHANICAL_ENGINEERING): ")
                    study_field = StudyField[field]
                    print(f"\nFaculties in the '{field}' field:")
                    for faculty in self.university.faculties:
                        if faculty.study_field == study_field:
                            print(f"{faculty.name} ({faculty.abbreviation})")
                case '5':
                    break
                case '6':
                    self.logger.log("Program ended.\n")
                    print("Exiting program. Goodbye!")
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    exit()
                case _:
                    self.logger.log("Invalid choice.")
                    print("Invalid choice.")