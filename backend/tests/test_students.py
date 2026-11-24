import sqlite3

from app import create_app
from conftest import add_student


# ---------- Create ----------

def test_create_student_returns_201_with_location(client):
    response = add_student(client)

    assert response.status_code == 201
    assert response.headers["Location"] == "/students/1630"
    assert response.get_json() == {"studentId": 1630, "name": "Rihan", "major": "EEE"}


def test_create_student_with_existing_id_returns_409(client):
    add_student(client)
    response = add_student(client, name="Someone Else")

    assert response.status_code == 409
    assert response.get_json()["type"] == "/problems/conflict"


def test_create_student_with_invalid_fields_returns_422_with_field_errors(client):
    response = client.post("/students", json={"studentId": -5, "name": "", "major": 42})

    assert response.status_code == 422
    assert response.content_type == "application/problem+json"
    body = response.get_json()
    pointers = [error["pointer"] for error in body["errors"]]
    assert pointers == ["/studentId", "/name", "/major"]
    assert body["detail"] == "3 fields are invalid."


def test_create_student_with_malformed_json_returns_400(client):
    response = client.post("/students", data='{"studentId": 1', content_type="application/json")

    assert response.status_code == 400
    assert response.get_json()["type"] == "/problems/bad-request"


# ---------- Read ----------

def test_get_student_returns_200(client):
    add_student(client)
    response = client.get("/students/1630")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Rihan"


def test_get_unknown_student_returns_404(client):
    response = client.get("/students/9999")

    assert response.status_code == 404
    assert response.get_json()["type"] == "/problems/not-found"


def test_list_students_in_id_order(client):
    add_student(client, 1654, "Akhar", "CSE")
    add_student(client, 1630, "Rihan", "EEE")
    response = client.get("/students")

    assert response.status_code == 200
    ids = [item["studentId"] for item in response.get_json()["items"]]
    assert ids == [1630, 1654]


def test_list_students_filtered_by_major(client):
    add_student(client, 1654, "Akhar", "CSE")
    add_student(client, 1630, "Rihan", "EEE")
    response = client.get("/students?major=CSE")

    items = response.get_json()["items"]
    assert len(items) == 1
    assert items[0]["name"] == "Akhar"


def test_list_students_with_unknown_filter_returns_400(client):
    response = client.get("/students?colour=blue")

    assert response.status_code == 400


def test_empty_list_returns_200_with_no_items(client):
    response = client.get("/students")

    assert response.status_code == 200
    assert response.get_json() == {"items": []}


# ---------- Update ----------

def test_replace_student_returns_200(client):
    add_student(client)
    response = client.put("/students/1630", json={"name": "Rihan Ahmed", "major": "CSE"})

    assert response.status_code == 200
    assert client.get("/students/1630").get_json()["major"] == "CSE"


def test_replace_unknown_student_returns_404(client):
    response = client.put("/students/9999", json={"name": "Nobody", "major": "CSE"})

    assert response.status_code == 404


def test_replace_student_with_missing_field_returns_422(client):
    add_student(client)
    response = client.put("/students/1630", json={"name": "Rihan"})

    assert response.status_code == 422
    assert response.get_json()["errors"][0]["pointer"] == "/major"


def test_replace_student_with_different_id_in_body_returns_422(client):
    add_student(client)
    response = client.put("/students/1630", json={"studentId": 1, "name": "Rihan", "major": "EEE"})

    assert response.status_code == 422


# ---------- Delete ----------

def test_delete_student_returns_204_then_404(client):
    add_student(client)

    assert client.delete("/students/1630").status_code == 204
    assert client.get("/students/1630").status_code == 404
    assert client.delete("/students/1630").status_code == 404


# ---------- Persistence ----------

def test_student_is_stored_in_the_database(client, db_path):
    add_student(client)

    connection = sqlite3.connect(db_path)
    row = connection.execute("SELECT name, major FROM students WHERE student_id = 1630").fetchone()
    connection.close()
    assert row == ("Rihan", "EEE")


def test_student_survives_an_app_restart(client, db_path):
    add_student(client)

    restarted_client = create_app({"DATABASE_PATH": db_path}).test_client()
    assert restarted_client.get("/students/1630").status_code == 200
