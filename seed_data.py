import random
from faker import Faker

from app.db import init_db
from app import models

fake = Faker()
random.seed(42)
Faker.seed(42)

COURSES = [
    ("Introduction to Programming", "CS101", 3),
    ("Data Structures & Algorithms", "CS201", 4),
    ("Database Systems", "CS301", 3),
    ("Calculus I", "MATH101", 4),
    ("Statistics", "MATH210", 3),
    ("English Composition", "ENG101", 3),
]

SEMESTER = "Fall2026"
ASSIGNMENTS = [
    ("Homework 1", 1.0),
    ("Homework 2", 1.0),
    ("Midterm Exam", 2.0),
    ("Final Exam", 3.0),
]


def seed():
    print("Initializing fresh database...")
    init_db()

    print("Creating courses...")
    course_ids = []
    for name, code, credits in COURSES:
        cid = models.add_course(name, code, credits)
        course_ids.append(cid)

    print("Creating 30 students...")
    student_ids = []
    for _ in range(30):
        first = fake.first_name()
        last = fake.last_name()
        email = f"{first.lower()}.{last.lower()}@example.edu"
        sid = models.add_student(first, last, email)
        student_ids.append(sid)

    print("Enrolling students and generating grades...")
    for sid in student_ids:
        my_courses = random.sample(course_ids, k=random.randint(3, 5))
        for cid in my_courses:
            enrollment_id = models.enroll_student(sid, cid, SEMESTER)
            skill = random.uniform(0.6, 0.98)
            for assignment_name, weight in ASSIGNMENTS:
                max_score = 100.0
                noise = random.uniform(-0.08, 0.08)
                score = max(0, min(100, round((skill + noise) * max_score, 1)))
                models.add_grade(enrollment_id, assignment_name, score, max_score, weight)

    print(f"Done. Seeded {len(student_ids)} students across {len(course_ids)} courses.")


if __name__ == "__main__":
    seed()
