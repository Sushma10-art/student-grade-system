PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    enrollment_date DATE DEFAULT CURRENT_DATE
);
CREATE TABLE courses (
    course_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name     TEXT NOT NULL,
    course_code     TEXT UNIQUE NOT NULL,
    credits         INTEGER NOT NULL CHECK (credits > 0)
);
CREATE TABLE enrollments (
    enrollment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    course_id       INTEGER NOT NULL,
    semester        TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE (student_id, course_id, semester)
);
CREATE TABLE grades (
    grade_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id   INTEGER NOT NULL,
    assignment_name TEXT NOT NULL,
    score           REAL NOT NULL CHECK (score >= 0),
    max_score       REAL NOT NULL CHECK (max_score > 0),
    weight          REAL NOT NULL DEFAULT 1.0 CHECK (weight > 0),
    FOREIGN KEY (enrollment_id) REFERENCES
enrollments(enrollment_id) ON DELETE CASCADE
);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_grades_enrollment ON grades(enrollment_id);
