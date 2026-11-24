import pytest

from app import create_app


@pytest.fixture
def db_path(tmp_path):
    # Every test gets its own empty database file; pytest deletes tmp_path afterwards
    return str(tmp_path / "test.db")


@pytest.fixture
def app(db_path):
    return create_app({"APP_ENV": "test", "DATABASE_PATH": db_path})


@pytest.fixture
def client(app):
    return app.test_client()


def add_student(client, student_id=1630, name="Rihan", major="EEE"):
    return client.post("/students", json={"studentId": student_id, "name": name, "major": major})
