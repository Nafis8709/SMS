from app.domain.student import Student


class StudentRepository:
    """The only code that reads or writes the students table."""

    def __init__(self, database):
        self.database = database

    def add(self, student):
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT INTO students (student_id, name, major) VALUES (?, ?, ?)",
                (student.student_id, student.name, student.major),
            )
            connection.commit()
        finally:
            connection.close()

    def get(self, student_id):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT student_id, name, major FROM students WHERE student_id = ?",
                (student_id,),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None
        return Student(row["student_id"], row["name"], row["major"])

    def list(self, major=None):
        connection = self.database.connect()
        try:
            if major is None:
                rows = connection.execute(
                    "SELECT student_id, name, major FROM students ORDER BY student_id"
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT student_id, name, major FROM students WHERE major = ? ORDER BY student_id",
                    (major,),
                ).fetchall()
        finally:
            connection.close()

        students = []
        for row in rows:
            students.append(Student(row["student_id"], row["name"], row["major"]))
        return students

    def save(self, student):
        connection = self.database.connect()
        try:
            connection.execute(
                "UPDATE students SET name = ?, major = ? WHERE student_id = ?",
                (student.name, student.major, student.student_id),
            )
            connection.commit()
        finally:
            connection.close()

    def delete(self, student_id):
        connection = self.database.connect()
        try:
            connection.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            connection.commit()
        finally:
            connection.close()
