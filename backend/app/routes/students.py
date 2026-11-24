from flask import Blueprint, current_app, jsonify, request

from app.routes.helpers import read_json, reject_unknown_params, student_to_json

bp = Blueprint("students", __name__, url_prefix="/students")


def _service():
    return current_app.extensions["student_service"]


@bp.post("")
def create_student():
    student = _service().create_student(read_json())

    response = jsonify(student_to_json(student))
    response.status_code = 201
    response.headers["Location"] = f"/students/{student.student_id}"
    return response


@bp.get("")
def list_students():
    reject_unknown_params(["major"])
    students = _service().list_students(request.args.get("major"))

    items = []
    for student in students:
        items.append(student_to_json(student))
    return jsonify({"items": items})


@bp.get("/<int:student_id>")
def get_student(student_id):
    student = _service().get_student(student_id)
    return jsonify(student_to_json(student))


@bp.put("/<int:student_id>")
def replace_student(student_id):
    student = _service().replace_student(student_id, read_json())
    return jsonify(student_to_json(student))


@bp.delete("/<int:student_id>")
def delete_student(student_id):
    _service().delete_student(student_id)
    return "", 204
