from flask import request

from app.errors import BadRequest


def read_json():
    """Return the request body as a dict, or raise 400 if it is not a JSON object."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise BadRequest("Request body must be a valid JSON object")
    return data


def reject_unknown_params(allowed):
    """Unknown query parameters are a client mistake, so they return 400."""
    for name in request.args:
        if name not in allowed:
            raise BadRequest(f"Unknown query parameter: {name}")


def student_to_json(student):
    return {
        "studentId": student.student_id,
        "name": student.name,
        "major": student.major,
    }
