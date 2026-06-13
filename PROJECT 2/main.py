import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

from models import Student
from utils import *

students = load_data(Student)


# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()
root.title("Smart Student Management System")
root.geometry("1000x700")


# ---------------- TITLE ---------------- #

title = tk.Label(
    root,
    text="SMART STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)


# ---------------- INPUT FRAME ---------------- #

input_frame = tk.Frame(root)
input_frame.pack(pady=10)


# Student ID

tk.Label(
    input_frame,
    text="Student ID"
).grid(row=0, column=0)

id_entry = tk.Entry(input_frame)
id_entry.grid(row=0, column=1)


# Name

tk.Label(
    input_frame,
    text="Name"
).grid(row=1, column=0)

name_entry = tk.Entry(input_frame)
name_entry.grid(row=1, column=1)


# Email

tk.Label(
    input_frame,
    text="Email"
).grid(row=2, column=0)

email_entry = tk.Entry(input_frame)
email_entry.grid(row=2, column=1)


# Phone

tk.Label(
    input_frame,
    text="Phone"
).grid(row=3, column=0)

phone_entry = tk.Entry(input_frame)
phone_entry.grid(row=3, column=1)


# Course

tk.Label(
    input_frame,
    text="Course"
).grid(row=4, column=0)

course_entry = tk.Entry(input_frame)
course_entry.grid(row=4, column=1)


# Branch

tk.Label(
    input_frame,
    text="Branch"
).grid(row=5, column=0)

branch_entry = tk.Entry(input_frame)
branch_entry.grid(row=5, column=1)


# ---------------- DISPLAY AREA ---------------- #

display_box = scrolledtext.ScrolledText(
    root,
    width=100,
    height=20
)

display_box.pack(pady=10)


# ---------------- REGISTER STUDENT ---------------- #

def register_student():

    sid = id_entry.get()
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    course = course_entry.get()
    branch = branch_entry.get()

    if sid == "" or name == "":
        messagebox.showerror(
            "Error",
            "ID and Name Required"
        )
        return

    for student in students:

        if student.student_id == sid:

            messagebox.showerror(
                "Error",
                "Duplicate Student ID"
            )

            return

    student = Student(
        sid,
        name,
        email,
        phone,
        course,
        branch
    )

    students.append(student)

    messagebox.showinfo(
        "Success",
        "Student Registered"
    )


# ---------------- VIEW STUDENTS ---------------- #

def view_students():

    display_box.delete(
        "1.0",
        tk.END
    )

    for student in students:

        display_box.insert(
            tk.END,
            f"""
ID : {student.student_id}
Name : {student.name}
Email : {student.email}
Phone : {student.phone}
Course : {student.course}
Branch : {student.branch}
Attendance : {student.attendance}
Fee : {student.fee_status}

----------------------------
"""
        )


# ---------------- SEARCH STUDENT ---------------- #

def search_student():

    sid = id_entry.get()

    student = recursive_search(
        students,
        sid
    )

    display_box.delete(
        "1.0",
        tk.END
    )

    if student:

        display_box.insert(
            tk.END,
            student.display_details()
        )

    else:

        display_box.insert(
            tk.END,
            "Student Not Found"
        )


# ---------------- ATTENDANCE ---------------- #

def mark_attendance():

    sid = id_entry.get()

    student = recursive_search(
        students,
        sid
    )

    if not student:

        messagebox.showerror(
            "Error",
            "Student Not Found"
        )
        return

    attendance_window = tk.Toplevel(root)

    attendance_window.title(
        "Attendance"
    )

    tk.Label(
        attendance_window,
        text="Attendance %"
    ).pack()

    attendance_entry = tk.Entry(
        attendance_window
    )

    attendance_entry.pack()


    def save_attendance():

        try:

            student.attendance = int(
                attendance_entry.get()
            )

            messagebox.showinfo(
                "Success",
                "Attendance Saved"
            )

            attendance_window.destroy()

        except:

            messagebox.showerror(
                "Error",
                "Invalid Input"
            )

    tk.Button(
        attendance_window,
        text="Save",
        command=save_attendance
    ).pack()

    # ---------------- ENTER MARKS ---------------- #

def enter_marks():

    sid = id_entry.get()

    student = recursive_search(
        students,
        sid
    )

    if not student:

        messagebox.showerror(
            "Error",
            "Student Not Found"
        )
        return

    marks_window = tk.Toplevel(root)

    marks_window.title("Enter Marks")

    tk.Label(
        marks_window,
        text="Subject"
    ).pack()

    subject_entry = tk.Entry(
        marks_window
    )
    subject_entry.pack()

    tk.Label(
        marks_window,
        text="Marks"
    ).pack()

    marks_entry = tk.Entry(
        marks_window
    )
    marks_entry.pack()

    def save_marks():

        try:

            subject = subject_entry.get()

            marks = int(
                marks_entry.get()
            )

            if marks < 0 or marks > 100:

                messagebox.showerror(
                    "Error",
                    "Marks should be between 0 and 100"
                )
                return

            student.add_marks(
                subject,
                marks
            )

            messagebox.showinfo(
                "Success",
                "Marks Saved"
            )

            marks_window.destroy()

        except:

            messagebox.showerror(
                "Error",
                "Invalid Marks"
            )

    tk.Button(
        marks_window,
        text="Save",
        command=save_marks
    ).pack(pady=10)


# ---------------- VIEW RESULT ---------------- #

def view_result():

    sid = id_entry.get()

    student = recursive_search(
        students,
        sid
    )

    display_box.delete(
        "1.0",
        tk.END
    )

    if not student:

        display_box.insert(
            tk.END,
            "Student Not Found"
        )
        return

    marks = student.get_marks()

    avg = student.average_marks()

    grade = student.calculate_grade(
        avg
    )

    display_box.insert(
        tk.END,
        f"\nResult Of {student.name}\n\n"
    )

    for subject, mark in marks.items():

        display_box.insert(
            tk.END,
            f"{subject} : {mark}\n"
        )

    display_box.insert(
        tk.END,
        f"\nAverage : {avg:.2f}"
    )

    display_box.insert(
        tk.END,
        f"\nGrade : {grade}"
    )


# ---------------- FEE MANAGEMENT ---------------- #

def fee_management():

    sid = id_entry.get()

    student = recursive_search(
        students,
        sid
    )

    if not student:

        messagebox.showerror(
            "Error",
            "Student Not Found"
        )
        return

    fee_window = tk.Toplevel(root)

    fee_window.title(
        "Fee Status"
    )

    def paid():

        student.fee_status = "Paid"

        messagebox.showinfo(
            "Success",
            "Fee Updated"
        )

        fee_window.destroy()

    def pending():

        student.fee_status = "Pending"

        messagebox.showinfo(
            "Success",
            "Fee Updated"
        )

        fee_window.destroy()

    tk.Button(
        fee_window,
        text="Paid",
        width=20,
        command=paid
    ).pack(pady=5)

    tk.Button(
        fee_window,
        text="Pending",
        width=20,
        command=pending
    ).pack(pady=5)


# ---------------- REPORTS ---------------- #

def generate_reports():

    generate_all_reports(
        students
    )

    messagebox.showinfo(
        "Success",
        "CSV Reports Generated"
    )


# ---------------- SAVE ---------------- #

def save_records():

    save_data(
        students
    )

    messagebox.showinfo(
        "Success",
        "Data Saved"
    )


# ---------------- LOAD ---------------- #

def load_records():

    global students

    students = load_data(
        Student
    )

    messagebox.showinfo(
        "Success",
        "Data Loaded"
    )


# ---------------- SORT BY MARKS ---------------- #

def show_toppers():

    display_box.delete(
        "1.0",
        tk.END
    )

    sorted_students = sort_by_marks(
        students
    )

    for student in sorted_students:

        display_box.insert(
            tk.END,
            f"{student.student_id} | "
            f"{student.name} | "
            f"{student.average_marks():.2f}\n"
        )


# ---------------- SORT BY ATTENDANCE ---------------- #

def show_attendance_rank():

    display_box.delete(
        "1.0",
        tk.END
    )

    sorted_students = sort_by_attendance(
        students
    )

    for student in sorted_students:

        display_box.insert(
            tk.END,
            f"{student.student_id} | "
            f"{student.name} | "
            f"{student.attendance}%\n"
        )


# ---------------- TOTAL STUDENTS ---------------- #

def show_total_students():

    total = Student.get_total_students()

    messagebox.showinfo(
        "Total Students",
        f"Total Students = {total}"
    )


# ---------------- BUTTON FRAME ---------------- #

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Register Student",
    width=20,
    command=register_student
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="View Students",
    width=20,
    command=view_students
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Search Student",
    width=20,
    command=search_student
).grid(row=0, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Mark Attendance",
    width=20,
    command=mark_attendance
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Enter Marks",
    width=20,
    command=enter_marks
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="View Result",
    width=20,
    command=view_result
).grid(row=1, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Fee Management",
    width=20,
    command=fee_management
).grid(row=2, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Generate Reports",
    width=20,
    command=generate_reports
).grid(row=2, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Save Data",
    width=20,
    command=save_records
).grid(row=2, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Load Data",
    width=20,
    command=load_records
).grid(row=3, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Topper List",
    width=20,
    command=show_toppers
).grid(row=3, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Attendance Rank",
    width=20,
    command=show_attendance_rank
).grid(row=3, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Total Students",
    width=20,
    command=show_total_students
).grid(row=4, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Exit",
    width=20,
    command=root.destroy
).grid(row=4, column=1, padx=5, pady=5)


# ---------------- START ---------------- #

root.mainloop()