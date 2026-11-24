"""Errors raised by services and the domain.

This module must not import Flask: the domain and services raise these errors,
and only the error handler in app/__init__.py turns them into HTTP responses.
"""


class AppError(Exception):
    status = 500
    title = "Internal server error"
    code = "internal-error"

    def __init__(self, detail, errors=None):
        super().__init__(detail)
        self.detail = detail
        self.errors = errors


class BadRequest(AppError):
    status = 400
    title = "Bad request"
    code = "bad-request"


class NotFound(AppError):
    status = 404
    title = "Resource not found"
    code = "not-found"


class Conflict(AppError):
    status = 409
    title = "Request conflicts with current state"
    code = "conflict"


class ValidationFailed(AppError):
    status = 422
    title = "Validation failed"
    code = "validation"
