# Student Grade Management System

A command-line application for managing students, courses, enrollments, and grades, built with Python and SQLite. Calculates weighted grade averages, GPA, and class rankings using SQL window functions.

## Features

- Add and manage students and courses
- Enroll students in courses per semester
- Record weighted grades (homework, midterms, finals, etc.)
- Calculate weighted percentage averages and GPA (credit-weighted, 4.0 scale)
- Rank students within a course using SQL RANK() window function
- Interactive CLI menu
- Seed script to populate realistic fake data (via Faker)
- Full test suite (pytest)

## Setup

pip install -r requirements.txt
python -m app.db

## Usage

Populate with sample data:

python seed_data.py

Run the interactive CLI:

python -m app.main

Run tests:

pytest tests/ -v

## Project structure

student-grade-system/
    app/
        db.py       - database connection and schema init
        models.py   - CRUD and analytical SQL queries
        main.py     - interactive CLI
    data/           - SQLite database (generated)
    tests/
        test_models.py - pytest suite
    schema.sql
    seed_data.py
    requirements.txt

## License

MIT

## Sample Output

Viewing a student report card (option 7):

Choose an option: 7
Student ID: 1
Semester filter (blank = all):
  CS101 - Introduction to Programming: 65.79% (GPA pts: 1.0, credits: 3)
  CS301 - Database Systems: 85.74% (GPA pts: 3.0, credits: 3)
  MATH101 - Calculus I: 66.36% (GPA pts: 1.0, credits: 4)
  MATH210 - Statistics: 90.99% (GPA pts: 3.7, credits: 3)
  ENG101 - English Composition: 60.54% (GPA pts: 0.0, credits: 3)
Overall GPA: 1.694

Viewing class ranking for a course (option 8):

Choose an option: 8
Course ID: 1
Semester filter (blank = all):
  #1: Robert Johnson - 97.7%
  #2: Jeffrey Lawrence - 96.11%
  #3: Matthew Moore - 92.17%
  #4: Joshua Walker - 91.0%
  #5: Jeremy Roberts - 86.86%
  #6: Jeffery Wagner - 86.19%
  #7: Jill Rhodes - 82.97%
  #8: Craig Ramirez - 81.27%
  #9: Patricia Miller - 78.0%
  #10: George Daniel - 77.79%
