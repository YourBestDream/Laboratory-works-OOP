class Faculty():
    def __init__(self,facultyName, abbreviation, students, studyField):
        self.facultyName = facultyName
        self.abbreviation = abbreviation
        self.students = []
        self.studyField = studyField
    
    def add_student(self, student):
        self.students.append(student)
    
    def graduate_student(self, student):
        if student in self.students:
            self.students.remove(student)