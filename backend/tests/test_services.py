"""Use cases run directly, without starting a web server (lecture slide 25)."""

import pytest

from app.errors import Conflict
from app.repositories.course_repository import CourseRepository
from app.repositories.database import Database
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.services.course_service import CourseService
from app.services.student_service import StudentService


@pytest.fixture
def services(db_path):
    database = Database(db_path)
    database.create_tables()
    student_repo = StudentRepository(database)
    course_repo = CourseRepository(database)
    enrollment_repo = EnrollmentRepository(database)
    return (
        StudentService(student_repo, enrollment_repo),
        CourseService(course_repo, student_repo, enrollment_repo),
    )


def test_last_seat_rule_without_http(services):
    student_service, course_service = services
    course_service.create_course({"code": "CSE3102", "title": "Web Technology Lab", "seats": 1})
    student_service.create_student({"studentId": 1630, "name": "Rihan", "major": "EEE"})
    student_service.create_student({"studentId": 1654, "name": "Akhar", "major": "CSE"})

    course_service.enroll("CSE3102", {"studentId": 1630})
    with pytest.raises(Conflict):
        course_service.enroll("CSE3102", {"studentId": 1654})


def test_unexpected_error_is_logged_but_hidden_from_client(app, client, caplog, monkeypatch):
    def broken_list(major=None):
        raise RuntimeError("database password is hunter2")

    monkeypatch.setattr(app.extensions["student_service"], "list_students", broken_list)
    response = client.get("/students")

    assert response.status_code == 500
    assert response.get_json()["detail"] == "Something went wrong"
    assert "hunter2" not in response.get_data(as_text=True)
    assert "hunter2" in caplog.text
