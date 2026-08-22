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
