class Menu:
    def __init__(self, university):
        self.university = university

    def run(self):
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
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    break
                case _:
                    print("Invalid choice.")

    def run_faculty_operations(self):
        while True:
            print("\n" + "=" * 30)
            print(" Faculty Operations")
            print("=" * 30)
            print("└─1. Create and assign a student to a faculty")
            print("└─2. Graduate a student from a faculty")
            print("└─3. Display current enrolled students")
            print("└─4. Display graduates")
            print("└─5. Check if a student belongs to this faculty")
            print("\n  6. Back to the main menu")
            print("  7. Exit the program")
            faculty_choice = input("Enter your choice: ")

            match faculty_choice:
                case '1':
                    self.university.assign_student_to_faculty()
                case '2':
                    self.university.graduate_student_from_faculty()
                case '3':
                    self.university.display_enrolled_students()
                case '4':
                    self.university.display_graduates()
                case '5':
                    self.university.check_student_belonging()
                case '6':
                    break
                case '7':
                    print("Exiting program. Goodbye!")
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    exit()
                case _:
                    print("Invalid choice.")

    def run_general_operations(self):
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
                    print("Exiting program. Goodbye!")
                    self.university.file_manager.save_faculties(self.university.faculties)
                    self.university.file_manager.save_students(self.university.students)
                    exit()
                case _:
                    print("Invalid choice.")