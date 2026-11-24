import sqlite3

from conftest import add_student


def add_course(client, code="CSE3102", title="Web Technology Lab", seats=2):
    return client.post("/courses", json={"code": code, "title": title, "seats": seats})


def enroll(client, student_id, code="CSE3102"):
    return client.post(f"/courses/{code}/enrollments", json={"studentId": student_id})


# ---------- Course CRUD ----------

def test_create_course_returns_201_with_location(client):
    response = add_course(client)

    assert response.status_code == 201
    assert response.headers["Location"] == "/courses/CSE3102"
    assert response.get_json() == {"code": "CSE3102", "title": "Web Technology Lab", "seats": 2}


def test_create_course_with_existing_code_returns_409(client):
    add_course(client)

    assert add_course(client).status_code == 409


def test_create_course_with_invalid_fields_returns_422(client):
    response = client.post("/courses", json={"code": "CSE 3102!", "title": "Web", "seats": 0})

    assert response.status_code == 422
    pointers = [error["pointer"] for error in response.get_json()["errors"]]
    assert pointers == ["/code", "/seats"]


def test_get_and_list_courses(client):
    add_course(client, "SWE101", "Intro", 10)
    add_course(client, "CSE3102")

    assert client.get("/courses/SWE101").get_json()["title"] == "Intro"
    codes = [item["code"] for item in client.get("/courses").get_json()["items"]]
    assert codes == ["CSE3102", "SWE101"]


def test_get_unknown_course_returns_404(client):
    assert client.get("/courses/NOPE1").status_code == 404


def test_replace_course_returns_200(client):
    add_course(client)
    response = client.put("/courses/CSE3102", json={"title": "Web Tech", "seats": 40})

    assert response.status_code == 200
    assert client.get("/courses/CSE3102").get_json()["seats"] == 40


def test_reducing_seats_below_enrolled_count_returns_409(client):
    add_course(client, seats=2)
    add_student(client, 1630)
    add_student(client, 1654)
    enroll(client, 1630)
    enroll(client, 1654)

    response = client.put("/courses/CSE3102", json={"title": "Web Technology Lab", "seats": 1})
    assert response.status_code == 409


def test_delete_course_returns_204_then_404(client):
    add_course(client)

    assert client.delete("/courses/CSE3102").status_code == 204
    assert client.get("/courses/CSE3102").status_code == 404


def test_delete_course_with_enrollments_returns_409(client):
    add_course(client)
    add_student(client)
    enroll(client, 1630)

    assert client.delete("/courses/CSE3102").status_code == 409


# ---------- Enrollment lifecycle ----------

def test_enroll_returns_201_and_can_be_read_back(client):
    add_course(client)
    add_student(client)
    response = enroll(client, 1630)

    assert response.status_code == 201
    assert response.headers["Location"] == "/courses/CSE3102/enrollments/1630"
    assert client.get(response.headers["Location"]).status_code == 200

    items = client.get("/courses/CSE3102/enrollments").get_json()["items"]
    assert items[0]["student"]["name"] == "Rihan"


def test_enrolling_twice_returns_409(client):
    add_course(client)
    add_student(client)
    enroll(client, 1630)
    response = enroll(client, 1630)

    assert response.status_code == 409
    assert response.get_json()["detail"] == "Student is already enrolled in this course"


def test_enrolling_in_a_full_course_returns_409(client):
    add_course(client, seats=1)
    add_student(client, 1630)
    add_student(client, 1654)
    enroll(client, 1630)
    response = enroll(client, 1654)

    assert response.status_code == 409
    assert response.get_json()["detail"] == "No seats left in this course"


def test_enrolling_unknown_student_returns_422(client):
    add_course(client)
    response = enroll(client, 9999)

    assert response.status_code == 422
    assert response.get_json()["errors"][0]["pointer"] == "/studentId"


def test_enrolling_in_unknown_course_returns_404(client):
    add_student(client)

    assert enroll(client, 1630, code="NOPE1").status_code == 404


def test_drop_returns_204_and_frees_the_seat(client):
    add_course(client, seats=1)
    add_student(client, 1630)
    add_student(client, 1654)
    enroll(client, 1630)

    assert client.delete("/courses/CSE3102/enrollments/1630").status_code == 204
    assert client.get("/courses/CSE3102/enrollments/1630").status_code == 404
    assert enroll(client, 1654).status_code == 201


def test_dropping_a_student_who_is_not_enrolled_returns_404(client):
    add_course(client)

    assert client.delete("/courses/CSE3102/enrollments/1630").status_code == 404


def test_deleting_an_enrolled_student_returns_409(client):
    add_course(client)
    add_student(client)
    enroll(client, 1630)

    assert client.delete("/students/1630").status_code == 409


# ---------- Persistence ----------

def test_enrollment_is_stored_in_the_database(client, db_path):
    add_course(client)
    add_student(client)
    enroll(client, 1630)

    connection = sqlite3.connect(db_path)
    rows = connection.execute("SELECT course_code, student_id FROM enrollments").fetchall()
    connection.close()
    assert rows == [("CSE3102", 1630)]
