import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app.db as db_module
from app import models


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test_grades.db"
    monkeypatch.setattr(db_module, "DB_PATH", test_db_path)
    db_module.init_db()
    yield


def test_add_and_get_student():
    sid = models.add_student("Test", "Student", "test@example.com")
    student = models.get_student(sid)
    assert student["first_name"] == "Test"
    assert student["last_name"] == "Student"


def test_list_students_empty_then_populated():
    assert models.list_students() == []
    models.add_student("Grace", "Hopper")
    students = models.list_students()
    assert len(students) == 1
    assert students[0]["first_name"] == "Grace"


def test_add_course():
    cid = models.add_course("Intro to CS", "CS101", 3)
    course = models.get_course(cid)
    assert course["course_code"] == "CS101"
    assert course["credits"] == 3


def test_enroll_student():
    sid = models.add_student("Ada", "Lovelace")
    cid = models.add_course("Math", "MATH101", 4)
    eid = models.enroll_student(sid, cid, "Fall2026")
    enrolled = models.list_enrollments_for_course(cid, "Fall2026")
    assert len(enrolled) == 1
    assert enrolled[0]["student_id"] == sid
    assert eid is not None


def test_duplicate_enrollment_raises():
    sid = models.add_student("Ada", "Lovelace")
    cid = models.add_course("Math", "MATH101", 4)
    models.enroll_student(sid, cid, "Fall2026")
    with pytest.raises(Exception):
        models.enroll_student(sid, cid, "Fall2026")


def test_weighted_average():
    sid = models.add_student("Ada", "Lovelace")
    cid = models.add_course("Math", "MATH101", 4)
    eid = models.enroll_student(sid, cid, "Fall2026")
    models.add_grade(eid, "Homework", 90, 100, weight=1.0)
    models.add_grade(eid, "Final Exam", 80, 100, weight=3.0)
    avg = models.weighted_average(eid)
    assert avg == pytest.approx(82.5)


def test_percentage_to_gpa_boundaries():
    assert models.percentage_to_gpa(95) == 4.0
    assert models.percentage_to_gpa(91) == 3.7
    assert models.percentage_to_gpa(60) == 0.0
    assert models.percentage_to_gpa(None) is None


def test_student_report_card_and_gpa():
    sid = models.add_student("Ada", "Lovelace")
    cid1 = models.add_course("Math", "MATH101", 4)
    cid2 = models.add_course("CS", "CS101", 3)
    eid1 = models.enroll_student(sid, cid1, "Fall2026")
    eid2 = models.enroll_student(sid, cid2, "Fall2026")
    models.add_grade(eid1, "Final", 95, 100, weight=1.0)
    models.add_grade(eid2, "Final", 85, 100, weight=1.0)
    report = models.student_report_card(sid, "Fall2026")
    assert len(report) == 2
    gpa = models.student_gpa(sid, "Fall2026")
    expected = round((4 * 4.0 + 3 * 3.0) / 7, 3)
    assert gpa == pytest.approx(expected)


def test_class_ranking_orders_correctly():
    cid = models.add_course("Math", "MATH101", 4)
    sid1 = models.add_student("High", "Scorer")
    sid2 = models.add_student("Low", "Scorer")
    eid1 = models.enroll_student(sid1, cid, "Fall2026")
    eid2 = models.enroll_student(sid2, cid, "Fall2026")
    models.add_grade(eid1, "Final", 95, 100)
    models.add_grade(eid2, "Final", 60, 100)
    ranking = models.class_ranking(cid, "Fall2026")
    assert ranking[0]["first_name"] == "High"
    assert ranking[0]["class_rank"] == 1
    assert ranking[1]["first_name"] == "Low"
    assert ranking[1]["class_rank"] == 2
