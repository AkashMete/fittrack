"""Consistent error envelope (API_DESIGN.md) via custom exceptions + centralized handlers."""
from flask import Flask
from marshmallow import ValidationError


class ApiError(Exception):
    status_code = 500
    code = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details

    def to_response(self):
        error = {"code": self.code, "message": self.message}
        if self.details:
            error["details"] = self.details
        return {"status": "error", "error": error}, self.status_code


class BadRequestError(ApiError):
    status_code = 400
    code = "BAD_REQUEST"


class UnauthorizedError(ApiError):
    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(ApiError):
    status_code = 403
    code = "FORBIDDEN"


class NotFoundError(ApiError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(ApiError):
    status_code = 409
    code = "CONFLICT"


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(e: ApiError):
        return e.to_response()

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return {
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": e.messages,
            },
        }, 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return {
            "status": "error",
            "error": {"code": "NOT_FOUND", "message": "Resource not found"},
        }, 404

    @app.errorhandler(429)
    def handle_rate_limit(e):
        return {
            "status": "error",
            "error": {"code": "RATE_LIMITED", "message": "Too many requests — slow down"},
        }, 429

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        if isinstance(e, (ApiError, ValidationError)):
            raise e
        app.logger.exception("Unhandled exception")  # always log 500s
        return {
            "status": "error",
            "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
        }, 500
