import random

class Student:
    def __init__(self, name):
        self.name = name
        self.uniform = None
        self.attendance = 0 
        self.is_good_student = True

    def dress_uniform(self, regiment_rules):
        self.uniform = regiment_rules

    def attend_class(self):
        self.attendance += 1

    def behave(self):
        self.is_good_student = random.choice([True, False])

    def __str__(self):
        return f"{self.name}: {'Good' if self.is_good_student else 'Not-So-Good'} Student, Uniform: {self.uniform}, Classes Attended: {self.attendance}"

regiment_rules = ["Uniform Shirt", "Uniform Pants", "Uniform Shoes", "Regimental Cap"]
student1 = Student("John Doe")
student1.dress_uniform(regiment_rules)
student1.attend_class()
student1.behave()

student2 = Student("Jane Smith")
student2.dress_uniform(regiment_rules)
student2.attend_class()
student2.behave()

print(student1)
print(student2)
