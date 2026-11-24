import sqlite3


class Database:
    """Opens SQLite connections and creates the tables. Only repositories use it."""

    def __init__(self, path):
        self.path = path

    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        connection = self.connect()
        try:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name       TEXT NOT NULL,
                    major      TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS courses (
                    code  TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    seats INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS enrollments (
                    course_code TEXT    NOT NULL REFERENCES courses (code),
                    student_id  INTEGER NOT NULL REFERENCES students (student_id),
                    PRIMARY KEY (course_code, student_id)
                );
                """
            )
            connection.commit()
        finally:
            connection.close()
