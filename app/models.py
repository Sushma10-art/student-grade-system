from app.db import get_connection


def add_student(first_name, last_name, email=None):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)",
        (first_name, last_name, email),
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def get_student(student_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM students WHERE student_id = ?", (student_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def list_students():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM students ORDER BY last_name, first_name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_course(course_name, course_code, credits):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO courses (course_name, course_code, credits) VALUES (?, ?, ?)",
        (course_name, course_code, credits),
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def list_courses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM courses ORDER BY course_code").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_course(course_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM courses WHERE course_id = ?", (course_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def enroll_student(student_id, course_id, semester):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO enrollments (student_id, course_id, semester) VALUES (?, ?, ?)",
        (student_id, course_id, semester),
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def list_enrollments_for_course(course_id, semester=None):
    conn = get_connection()
    query = """
        SELECT e.enrollment_id, s.student_id, s.first_name, s.last_name, e.semester
        FROM enrollments e
        JOIN students s ON s.student_id = e.student_id
        WHERE e.course_id = ?
    """
    params = [course_id]
    if semester:
        query += " AND e.semester = ?"
        params.append(semester)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_grade(enrollment_id, assignment_name, score, max_score, weight=1.0):
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO grades (enrollment_id, assignment_name, score, max_score, weight)
           VALUES (?, ?, ?, ?, ?)""",
        (enrollment_id, assignment_name, score, max_score, weight),
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def weighted_average(enrollment_id):
    conn = get_connection()
    row = conn.execute(
        """SELECT SUM((score / max_score) * weight) / SUM(weight) * 100 AS weighted_avg
           FROM grades WHERE enrollment_id = ?""",
        (enrollment_id,),
    ).fetchone()
    conn.close()
    return row["weighted_avg"] if row and row["weighted_avg"] is not None else None


def percentage_to_gpa(pct):
    if pct is None:
        return None
    if pct >= 93:
        return 4.0
    if pct >= 90:
        return 3.7
    if pct >= 87:
        return 3.3
    if pct >= 83:
        return 3.0
    if pct >= 80:
        return 2.7
    if pct >= 77:
        return 2.3
    if pct >= 73:
        return 2.0
    if pct >= 70:
        return 1.7
    if pct >= 67:
        return 1.3
    if pct >= 65:
        return 1.0
    return 0.0


def student_report_card(student_id, semester=None):
    conn = get_connection()
    query = """
        SELECT e.enrollment_id, c.course_name, c.course_code, c.credits, e.semester
        FROM enrollments e
        JOIN courses c ON c.course_id = e.course_id
        WHERE e.student_id = ?
    """
    params = [student_id]
    if semester:
        query += " AND e.semester = ?"
        params.append(semester)
    enrollments = conn.execute(query, params).fetchall()
    conn.close()

    report = []
    for e in enrollments:
        avg = weighted_average(e["enrollment_id"])
        gpa_points = percentage_to_gpa(avg)
        report.append({
            "course_name": e["course_name"],
            "course_code": e["course_code"],
            "credits": e["credits"],
            "semester": e["semester"],
            "average_pct": round(avg, 2) if avg is not None else None,
            "gpa_points": gpa_points,
        })
    return report


def student_gpa(student_id, semester=None):
    report = student_report_card(student_id, semester)
    total_credits = sum(r["credits"] for r in report if r["gpa_points"] is not None)
    if total_credits == 0:
        return None
    total_points = sum(r["credits"] * r["gpa_points"] for r in report if r["gpa_points"] is not None)
    return round(total_points / total_credits, 3)


def class_ranking(course_id, semester=None):
    conn = get_connection()
    query = """
        WITH student_avg AS (
            SELECT
                e.enrollment_id, s.first_name, s.last_name,
                SUM((g.score / g.max_score) * g.weight) / SUM(g.weight) * 100 AS avg_pct
            FROM enrollments e
            JOIN students s ON s.student_id = e.student_id
            JOIN grades g ON g.enrollment_id = e.enrollment_id
            WHERE e.course_id = ?
    """
    params = [course_id]
    if semester:
        query += " AND e.semester = ?"
        params.append(semester)
    query += """
            GROUP BY e.enrollment_id
        )
        SELECT first_name, last_name, ROUND(avg_pct, 2) AS avg_pct,
               RANK() OVER (ORDER BY avg_pct DESC) AS class_rank
        FROM student_avg ORDER BY class_rank
    """
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
