import json
import csv
import os


# ---------------- SAVE DATA ---------------- #

def save_data(students):

    data = []

    for student in students:

        data.append(
            {
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
                "course": student.course,
                "branch": student.branch,
                "attendance": student.attendance,
                "fee_status": student.fee_status,
                "marks": student.get_marks()
            }
        )

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


# ---------------- LOAD DATA ---------------- #

def load_data(Student):

    students = []

    if not os.path.exists("data.json"):
        return students

    with open("data.json", "r") as file:

        data = json.load(file)

        for item in data:

            student = Student(
                item["student_id"],
                item["name"],
                item["email"],
                item["phone"],
                item["course"],
                item["branch"]
            )

            student.attendance = item["attendance"]
            student.fee_status = item["fee_status"]

            marks = item["marks"]

            for subject, mark in marks.items():
                student.add_marks(subject, mark)

            students.append(student)

    return students


# ---------------- RECURSIVE SEARCH ---------------- #

def recursive_search(students, sid, index=0):

    if index >= len(students):
        return None

    if students[index].student_id == sid:
        return students[index]

    return recursive_search(
        students,
        sid,
        index + 1
    )


# ---------------- SORT BY MARKS ---------------- #

def sort_by_marks(students):

    return sorted(
        students,
        key=lambda s: s.average_marks(),
        reverse=True
    )


# ---------------- SORT BY ATTENDANCE ---------------- #

def sort_by_attendance(students):

    return sorted(
        students,
        key=lambda s: s.attendance,
        reverse=True
    )


# ---------------- TOPPERS ---------------- #

def get_toppers(students):

    toppers = [
        s for s in students
        if s.average_marks() >= 75
    ]

    return toppers


# ---------------- DEFAULTERS ---------------- #

def get_defaulters(students):

    defaulters = [
        s for s in students
        if s.attendance < 75
    ]

    return defaulters


# ---------------- ATTENDANCE CSV ---------------- #

def attendance_report(students):

    with open(
        "attendance.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Name",
            "Attendance"
        ])

        for student in students:

            writer.writerow([
                student.student_id,
                student.name,
                student.attendance
            ])


# ---------------- RESULT CSV ---------------- #

def result_report(students):

    with open(
        "result.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Name",
            "Average",
            "Grade"
        ])

        for student in students:

            avg = student.average_marks()

            grade = student.calculate_grade(avg)

            writer.writerow([
                student.student_id,
                student.name,
                avg,
                grade
            ])


# ---------------- FEE CSV ---------------- #

def fee_report(students):

    with open(
        "fee.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Name",
            "Fee Status"
        ])

        for student in students:

            writer.writerow([
                student.student_id,
                student.name,
                student.fee_status
            ])


# ---------------- OVERALL REPORT ---------------- #

def generate_all_reports(students):

    attendance_report(students)

    result_report(students)

    fee_report(students)


# ---------------- TOTAL STUDENTS ---------------- #

def total_students(students):
    return len(students)