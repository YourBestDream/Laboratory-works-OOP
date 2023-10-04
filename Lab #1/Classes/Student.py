class Student:
    def __init__(self, firstName, lastName, email, idnum, facultyAbbreviation, enrollmentDate, dateOfBirth, graduate):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.idnum = idnum
        self.facultyAbbreviation = facultyAbbreviation
        self.enrollmentDate = enrollmentDate
        self.dateOfBirth = dateOfBirth
        self.graduate = graduate

    def to_string(self):
        return f"{self.firstName},{self.lastName},{self.email},{self.idnum},{self.facultyAbbreviation},{self.enrollmentDate},{self.dateOfBirth},{self.graduate}"

    @staticmethod
    def from_string(string):
        fields = string.split(',')
        return Student(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7])