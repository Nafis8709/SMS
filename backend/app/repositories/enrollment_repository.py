from app.domain.student import Student


class EnrollmentRepository:
    """The only code that reads or writes the enrollments table."""

    def __init__(self, database):
        self.database = database

    def add(self, course_code, student_id):
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT INTO enrollments (course_code, student_id) VALUES (?, ?)",
                (course_code, student_id),
            )
            connection.commit()
        finally:
            connection.close()

    def exists(self, course_code, student_id):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT 1 FROM enrollments WHERE course_code = ? AND student_id = ?",
                (course_code, student_id),
            ).fetchone()
        finally:
            connection.close()
        return row is not None

    def count_for_course(self, course_code):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM enrollments WHERE course_code = ?",
                (course_code,),
            ).fetchone()
        finally:
            connection.close()
        return row["total"]

    def count_for_student(self, student_id):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM enrollments WHERE student_id = ?",
                (student_id,),
            ).fetchone()
        finally:
            connection.close()
        return row["total"]

    def list_students(self, course_code):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT s.student_id, s.name, s.major
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                WHERE e.course_code = ?
                ORDER BY s.student_id
                """,
                (course_code,),
            ).fetchall()
        finally:
            connection.close()

        students = []
        for row in rows:
            students.append(Student(row["student_id"], row["name"], row["major"]))
        return students

    def delete(self, course_code, student_id):
        connection = self.database.connect()
        try:
            connection.execute(
                "DELETE FROM enrollments WHERE course_code = ? AND student_id = ?",
                (course_code, student_id),
            )
            connection.commit()
        finally:
            connection.close()
