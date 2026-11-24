from flask import Blueprint, current_app, jsonify

from app.routes.helpers import read_json, reject_unknown_params, student_to_json

bp = Blueprint("courses", __name__, url_prefix="/courses")


def _service():
    return current_app.extensions["course_service"]


def course_to_json(course):
    return {"code": course.code, "title": course.title, "seats": course.seats}


def enrollment_to_json(code, student):
    return {"courseCode": code, "student": student_to_json(student)}


# ---------- Courses ----------

@bp.post("")
def create_course():
    course = _service().create_course(read_json())

    response = jsonify(course_to_json(course))
    response.status_code = 201
    response.headers["Location"] = f"/courses/{course.code}"
    return response


@bp.get("")
def list_courses():
    reject_unknown_params([])

    items = []
    for course in _service().list_courses():
        items.append(course_to_json(course))
    return jsonify({"items": items})


@bp.get("/<code>")
def get_course(code):
    return jsonify(course_to_json(_service().get_course(code)))


@bp.put("/<code>")
def replace_course(code):
    course = _service().replace_course(code, read_json())
    return jsonify(course_to_json(course))


@bp.delete("/<code>")
def delete_course(code):
    _service().delete_course(code)
    return "", 204


# ---------- Enrollments (sub-collection of a course) ----------

@bp.post("/<code>/enrollments")
def enroll(code):
    student = _service().enroll(code, read_json())

    response = jsonify(enrollment_to_json(code, student))
    response.status_code = 201
    response.headers["Location"] = f"/courses/{code}/enrollments/{student.student_id}"
    return response


@bp.get("/<code>/enrollments")
def list_enrollments(code):
    reject_unknown_params([])

    items = []
    for student in _service().list_enrollments(code):
        items.append(enrollment_to_json(code, student))
    return jsonify({"items": items})


@bp.get("/<code>/enrollments/<int:student_id>")
def get_enrollment(code, student_id):
    student = _service().get_enrollment(code, student_id)
    return jsonify(enrollment_to_json(code, student))


@bp.delete("/<code>/enrollments/<int:student_id>")
def drop(code, student_id):
    _service().drop(code, student_id)
    return "", 204
