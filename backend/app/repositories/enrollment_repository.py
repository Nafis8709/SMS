class EnrollmentRepository:
    """The only code that reads or writes the enrollments table."""

    def __init__(self, database):
        self.database = database

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
