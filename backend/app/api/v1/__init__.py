"""API v1 — versioned from day one so /api/v2 can ship without breaking clients."""
from flask import Blueprint
from flask_restx import Api
from marshmallow import ValidationError

from ...common.errors import ApiError

blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Paste: Bearer <access_token>",
    }
}

api = Api(
    blueprint,
    version="1.0",
    title="FitTrack API",
    description="Personal fitness tracking REST API",
    doc="/docs",
    authorizations=authorizations,
    security="Bearer",
)

from .auth.routes import auth_ns  # noqa: E402
from .users.routes import users_ns  # noqa: E402
from .foods.routes import foods_ns  # noqa: E402
from .diet.routes import diet_ns  # noqa: E402

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(users_ns, path="/users")
api.add_namespace(foods_ns, path="/foods")
api.add_namespace(diet_ns, path="/diet")


# flask-restx intercepts exceptions raised inside Resources — mirror the
# global handlers here so the envelope stays consistent either way.
@api.errorhandler(ApiError)
def handle_api_error(e: ApiError):
    body, code = e.to_response()
    return body, code


@api.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return {
        "status": "error",
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "details": e.messages,
        },
    }, 400
