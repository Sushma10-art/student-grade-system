from app import models
from app.db import init_db, DB_PATH


def menu_add_student():
    first = input("First name: ").strip()
    last = input("Last name: ").strip()
    email = input("Email (optional): ").strip() or None
    student_id = models.add_student(first, last, email)
    print(f"Added student #{student_id}: {first} {last}")


def menu_list_students():
    students = models.list_students()
    if not students:
        print("No students yet.")
        return
    for s in students:
        print(f"  [{s['student_id']}] {s['first_name']} {s['last_name']} ({s['email']})")


def menu_add_course():
    name = input("Course name: ").strip()
    code = input("Course code (e.g. CS101): ").strip()
    credits = int(input("Credits: ").strip())
    course_id = models.add_course(name, code, credits)
    print(f"Added course #{course_id}: {code} - {name}")


def menu_list_courses():
    courses = models.list_courses()
    if not courses:
        print("No courses yet.")
        return
    for c in courses:
        print(f"  [{c['course_id']}] {c['course_code']} - {c['course_name']} ({c['credits']} credits)")


def menu_enroll_student():
    menu_list_students()
    student_id = int(input("Student ID to enroll: ").strip())
    menu_list_courses()
    course_id = int(input("Course ID: ").strip())
    semester = input("Semester (e.g. Fall2026): ").strip()
    enrollment_id = models.enroll_student(student_id, course_id, semester)
    print(f"Enrolled. Enrollment ID = {enrollment_id}")


def menu_add_grade():
    enrollment_id = int(input("Enrollment ID: ").strip())
    assignment = input("Assignment name (e.g. Midterm): ").strip()
    score = float(input("Score achieved: ").strip())
    max_score = float(input("Max possible score: ").strip())
    weight = input("Weight (default 1.0): ").strip()
    weight = float(weight) if weight else 1.0
    models.add_grade(enrollment_id, assignment, score, max_score, weight)
    print("Grade recorded.")


def menu_report_card():
    student_id = int(input("Student ID: ").strip())
    semester = input("Semester filter (blank = all): ").strip() or None
    report = models.student_report_card(student_id, semester)
    if not report:
        print("No enrollments found.")
        return
    for r in report:
        print(f"  {r['course_code']} - {r['course_name']}: {r['average_pct']}% (GPA pts: {r['gpa_points']}, credits: {r['credits']})")
    gpa = models.student_gpa(student_id, semester)
    print(f"\nOverall GPA: {gpa}")


def menu_class_ranking():
    course_id = int(input("Course ID: ").strip())
    semester = input("Semester filter (blank = all): ").strip() or None
    ranking = models.class_ranking(course_id, semester)
    if not ranking:
        print("No grades recorded for this course yet.")
        return
    for r in ranking:
        print(f"  #{r['class_rank']}: {r['first_name']} {r['last_name']} - {r['avg_pct']}%")


MENU = """
=== Student Grade Management System ===
 1. Add Student
 2. List Students
 3. Add Course
 4. List Courses
 5. Enroll Student in Course
 6. Add Grade
 7. View Student Report Card (+ GPA)
 8. View Class Ranking
 0. Exit
"""

ACTIONS = {
    "1": menu_add_student,
    "2": menu_list_students,
    "3": menu_add_course,
    "4": menu_list_courses,
    "5": menu_enroll_student,
    "6": menu_add_grade,
    "7": menu_report_card,
    "8": menu_class_ranking,
}


def main():
    if not DB_PATH.exists():
        print("No database found, initializing...")
        init_db()

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice in ACTIONS:
            try:
                ACTIONS[choice]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid option.")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
