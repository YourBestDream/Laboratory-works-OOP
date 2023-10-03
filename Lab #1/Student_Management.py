from Faculty import Faculty
from Student import Student
from Study_Field import StudyField
# Faculty operations:
# 1. Create and assign a student to a faculty.
# 2. Graduate a student from a faculty.
# 3. Display current enrolled students (Graduates would be ignored).
# 4. Display graduates (Currently enrolled students would be ignored).
# 5. Tell or not if a student belongs to this faculty.
# • General operations:
# 1. Create a new faculty.
# 2. Search what faculty a student belongs to by a unique identifier (for example by email
# or a unique ID).
# 3. Display University faculties.
# 4. Display all faculties belonging to a field. (Ex. FOOD_TECHNOLOGY)

inp = input("Welcome to TUM's student management system! \n What do you want to do? \n g - General operations \n f - Faculty operations \n S - Student operations \n q - Quit Program \n your input> ")

faculties = []
students = []

while inp != "q":
    match(inp):
        case("g"):
            print(" cr - Create a new Faculty \n s - Search what faculty a student belongs to by ID \n d - Display University faculties \n f - Display all faculties belonging to a field. (Ex. FOOD_TECHNOLOGY) \n \n b - Back \n q - Quit program")
            inp = input(" your input> ")
            match(inp):
                case("cr"):
                    facultyName = input("Faculty name: ")
                    abbreviation = input("Faculty abbreviation: ")
                    StudyField = input("Faculty study field: ")
                    faculty = Faculty(facultyName, abbreviation, [], StudyField)
                    faculties.append(faculty)
                case("s"):
                    ident = input("Student ID: ")
                    for faculty in faculties:
                        for student in faculty.students:
                            if student.id == ident:
                                print("Student " , student.firstName , " " , student.lastName , " belongs to faculty " , faculty.facultyName)
                case ("d"):
                    pass

                case ("f"):
                    pass

                case ("b"):
                    print(" cr - Create a new Faculty \n s - Search what faculty a student belongs to by ID \n d - Display University faculties \n f - Display all faculties belonging to a field. (Ex. FOOD_TECHNOLOGY) \n \n b - Back \n q - Quit program")
                    inp = input(" your input> ")

                case("q"):
                    exit()
        case("f"):
            pass
        case("s"):
            pass
    print("Welcome to TUM's student management system! \n What do you want to do? \n g - General operations \n f - Faculty operations \n S - Student operations \n q - Quit Program")
    inp = input(" your input> ")