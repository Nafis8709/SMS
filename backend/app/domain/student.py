from dataclasses import dataclass

from app.domain.validation import failure_detail, field_error, is_positive_int, is_text
from app.errors import ValidationFailed

MAX_NAME_LENGTH = 100
MAX_MAJOR_LENGTH = 50


@dataclass
class Student:
    student_id: int
    name: str
    major: str


def parse_student(data, student_id=None):
    """Build a Student from request data, or raise ValidationFailed.

    On create (POST) the ID comes from the body.
    On replace (PUT) the ID comes from the URL and is passed in as student_id.
    """
    errors = []

    if student_id is None:
        student_id = data.get("studentId")
        if not is_positive_int(student_id):
            errors.append(field_error("/studentId", "must be a positive integer"))
    elif "studentId" in data and data["studentId"] != student_id:
        errors.append(field_error("/studentId", "must match the student ID in the URL"))

    name = data.get("name")
    if not is_text(name, MAX_NAME_LENGTH):
        errors.append(field_error("/name", f"must be a non-empty string of at most {MAX_NAME_LENGTH} characters"))

    major = data.get("major")
    if not is_text(major, MAX_MAJOR_LENGTH):
        errors.append(field_error("/major", f"must be a non-empty string of at most {MAX_MAJOR_LENGTH} characters"))

    if errors:
        raise ValidationFailed(failure_detail(errors), errors)

    return Student(student_id, name.strip(), major.strip())
