from abc import ABC, abstractmethod


# ---------------- DECORATOR ---------------- #

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} executed")
        return func(*args, **kwargs)
    return wrapper


# ---------------- ABSTRACT CLASS ---------------- #

class Person(ABC):

    def __init__(self, person_id, name, email, phone):
        self.person_id = person_id
        self.name = name
        self.email = email
        self.phone = phone

    @abstractmethod
    def display_details(self):
        pass


# ---------------- STUDENT ---------------- #

class Student(Person):

    total_students = 0

    def __init__(self, student_id, name, email, phone,
                 course, branch):

        super().__init__(student_id, name, email, phone)

        self.student_id = student_id
        self.course = course
        self.branch = branch

        self.attendance = 0
        self.fee_status = "Pending"

        # Encapsulation
        self.__marks = {}

        Student.total_students += 1

    def add_marks(self, subject, marks):
        self.__marks[subject] = marks

    def get_marks(self):
        return self.__marks

    def average_marks(self):

        if len(self.__marks) == 0:
            return 0

        return sum(self.__marks.values()) / len(self.__marks)

    @staticmethod
    def calculate_grade(avg):

        if avg >= 90:
            return "A+"

        elif avg >= 75:
            return "A"

        elif avg >= 60:
            return "B"

        elif avg >= 40:
            return "C"

        return "F"

    @classmethod
    def get_total_students(cls):
        return cls.total_students

    def display_details(self):

        return (
            f"ID: {self.student_id}\n"
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Course: {self.course}\n"
            f"Branch: {self.branch}\n"
        )

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def __repr__(self):
        return self.__str__()


# ---------------- FACULTY ---------------- #

class Faculty(Person):

    def __init__(self, faculty_id, name, email, phone,
                 department):

        super().__init__(faculty_id, name, email, phone)

        self.department = department

    def display_details(self):

        return (
            f"Faculty ID: {self.person_id}\n"
            f"Name: {self.name}\n"
            f"Department: {self.department}"
        )


# ---------------- COURSE ---------------- #

class Course:

    def __init__(self, course_id, course_name, credits):

        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits

    def __str__(self):
        return self.course_name


# ---------------- REPORT GENERATOR ---------------- #

def report_generator(students):

    for student in students:
        yield student