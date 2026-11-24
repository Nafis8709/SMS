from app.domain.course import Course


class CourseRepository:
    """The only code that reads or writes the courses table."""

    def __init__(self, database):
        self.database = database

    def add(self, course):
        connection = self.database.connect()
        try:
            connection.execute(
                "INSERT INTO courses (code, title, seats) VALUES (?, ?, ?)",
                (course.code, course.title, course.seats),
            )
            connection.commit()
        finally:
            connection.close()

    def get(self, code):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT code, title, seats FROM courses WHERE code = ?",
                (code,),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None
        return Course(row["code"], row["title"], row["seats"])

    def list(self):
        connection = self.database.connect()
        try:
            rows = connection.execute("SELECT code, title, seats FROM courses ORDER BY code").fetchall()
        finally:
            connection.close()

        courses = []
        for row in rows:
            courses.append(Course(row["code"], row["title"], row["seats"]))
        return courses

    def save(self, course):
        connection = self.database.connect()
        try:
            connection.execute(
                "UPDATE courses SET title = ?, seats = ? WHERE code = ?",
                (course.title, course.seats, course.code),
            )
            connection.commit()
        finally:
            connection.close()

    def delete(self, code):
        connection = self.database.connect()
        try:
            connection.execute("DELETE FROM courses WHERE code = ?", (code,))
            connection.commit()
        finally:
            connection.close()
