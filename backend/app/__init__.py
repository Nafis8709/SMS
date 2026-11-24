import logging
import uuid

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.errors import AppError
from app.repositories.database import Database
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.routes import students
from app.services.student_service import StudentService

log = logging.getLogger("app.http")
error_log = logging.getLogger("app.errors")


def create_app(overrides=None):
    config = Config(overrides)
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    app = Flask(__name__)

    # Wiring: the only place that chooses concrete classes
    database = Database(config.DATABASE_PATH)
    database.create_tables()
    student_repo = StudentRepository(database)
    enrollment_repo = EnrollmentRepository(database)

    app.extensions["student_service"] = StudentService(student_repo, enrollment_repo)
    app.register_blueprint(students.bp)

    register_middleware(app)
    register_error_handlers(app)
    return app


def register_middleware(app):
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]

    @app.after_request
    def log_request(response):
        response.headers["X-Request-ID"] = g.request_id
        log.info(
            "%s %s -> %s [%s]",
            request.method,
            request.path,
            response.status_code,
            g.request_id,
        )
        return response


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return problem(error.status, error.title, error.detail, error.code, error.errors)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        # Framework errors (unknown URL, wrong method) use the same format
        code = error.name.lower().replace(" ", "-")
        response = problem(error.code, error.name, error.description, code)
        if error.code == 405 and error.valid_methods:
            response.headers["Allow"] = ", ".join(error.valid_methods)
        return response

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        # Full stack trace goes to the log, never to the client
        error_log.exception("unhandled error [%s]", g.get("request_id"))
        return problem(500, "Internal server error", "Something went wrong", "internal-error")


def problem(status, title, detail, code, errors=None):
    """Build an RFC 9457 Problem Details response."""
    body = {
        "type": "/problems/" + code,
        "title": title,
        "status": status,
        "detail": detail,
        "requestId": g.get("request_id"),
    }
    if errors:
        body["errors"] = errors

    response = jsonify(body)
    response.status_code = status
    response.content_type = "application/problem+json"
    return response
