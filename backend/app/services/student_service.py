import logging

from app.domain.student import parse_student
from app.errors import Conflict, NotFound

log = logging.getLogger(__name__)


class StudentService:
    """Student use cases. Knows nothing about HTTP, JSON or status codes."""

    def __init__(self, student_repo, enrollment_repo):
        self.student_repo = student_repo
        self.enrollment_repo = enrollment_repo

    def create_student(self, data):
        student = parse_student(data)
        if self.student_repo.get(student.student_id) is not None:
            raise Conflict(f"A student with ID {student.student_id} already exists")

        self.student_repo.add(student)
        log.info("student created id=%s", student.student_id)
        return student

    def list_students(self, major=None):
        return self.student_repo.list(major)

    def get_student(self, student_id):
        student = self.student_repo.get(student_id)
        if student is None:
            raise NotFound(f"No student with ID {student_id}")
        return student

    def replace_student(self, student_id, data):
        self.get_student(student_id)  # 404 is checked before validation
        student = parse_student(data, student_id)

        self.student_repo.save(student)
        log.info("student updated id=%s", student_id)
        return student

    def delete_student(self, student_id):
        self.get_student(student_id)
        if self.enrollment_repo.count_for_student(student_id) > 0:
            raise Conflict("Student is still enrolled in a course; drop the enrollments first")

        self.student_repo.delete(student_id)
        log.info("student deleted id=%s", student_id)
